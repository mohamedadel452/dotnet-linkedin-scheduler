#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated LinkedIn Publisher for Mohamed Adel's .NET Engineering Journey
Works both locally (via linkedin_config.json) and 24/7 in the cloud via GitHub Actions Secrets!
"""
import os
import sys
import json
import argparse
import datetime
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(BASE_DIR, "posts_queue.json")
CONFIG_FILE = os.path.join(BASE_DIR, "linkedin_config.json")
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_person_urn(access_token):
    """Fetch the authenticated user's LinkedIn Person URN using /v2/userinfo or /v2/me."""
    for endpoint, key in [("https://api.linkedin.com/v2/userinfo", "sub"), ("https://api.linkedin.com/v2/me", "id")]:
        req = urllib.request.Request(
            endpoint,
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Restli-Protocol-Version": "2.0.0"
            }
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if key in data and data[key]:
                    return f"urn:li:person:{data[key]}"
        except urllib.error.HTTPError:
            continue
    raise RuntimeError("تعذر استخراج معرّف الحساب (Person URN) من LinkedIn API.")


def upload_image_to_linkedin(access_token, person_urn, image_path):
    """Register image upload and PUT binary image to LinkedIn."""
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    req = urllib.request.Request(
        register_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        reg_data = json.loads(resp.read().decode("utf-8"))

    upload_url = reg_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_urn = reg_data["value"]["asset"]

    with open(image_path, "rb") as img_f:
        img_bytes = img_f.read()

    put_req = urllib.request.Request(
        upload_url,
        data=img_bytes,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/octet-stream"
        },
        method="PUT"
    )
    with urllib.request.urlopen(put_req) as put_resp:
        _ = put_resp.read()

    return asset_urn


def format_bilingual_post(post):
    """Format a clean, natural, handwritten-style Arabic developer post without AI-looking formatting."""
    BLANK = "\u2800"
    parts = [
        post["arabic_text"].strip(),
        BLANK,
    ]
    if post.get("live_guide_url"):
        parts.extend([
            "الكود على GitHub:",
            post["repo_url"].strip(),
            BLANK,
            "الملخص التفاعلي (Live HTML):",
            post["live_guide_url"].strip(),
            BLANK,
        ])
    else:
        parts.extend([
            "حسابي على GitHub:",
            post["repo_url"].strip(),
            BLANK,
        ])
    parts.append(post["hashtags"].strip())
    return "\n".join(parts)


def publish_post_to_linkedin(access_token, person_urn, post_text, asset_urn=None, title=""):
    """Publish UGC post (with image if available, otherwise article/text share)."""
    url = "https://api.linkedin.com/v2/ugcPosts"
    share_content = {
        "shareCommentary": {
            "text": post_text
        },
        "shareMediaCategory": "IMAGE" if asset_urn else "NONE"
    }
    if asset_urn:
        share_content["media"] = [
            {
                "status": "READY",
                "description": {"text": title or ".NET Engineering Study Guide"},
                "media": asset_urn,
                "title": {"text": title or ".NET Engineering Journey"}
            }
        ]

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": share_content
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_email_notification(config, post, post_urn):
    """Send an email notification if smtp/email is configured via env vars or linkedin_config.json."""
    import smtplib
    from email.message import EmailMessage

    notify_to = (os.environ.get("NOTIFY_EMAIL") or config.get("notify_email") or "").strip()
    smtp_user = (os.environ.get("SMTP_USER") or config.get("smtp_user") or notify_to).strip()
    smtp_pass = (os.environ.get("SMTP_APP_PASSWORD") or config.get("smtp_app_password") or "").strip()
    if not (notify_to and smtp_pass):
        return False

    post_url = f"https://www.linkedin.com/feed/update/{post_urn}/"
    msg = EmailMessage()
    msg["Subject"] = f"✅ تم نشر منشورك على LinkedIn: {post['title']}"
    msg["From"] = smtp_user
    msg["To"] = notify_to
    msg.set_content(
        f"مرحباً محمد،\n\n"
        f"تم بنجاح نشر منشورك الجديد على LinkedIn تلقائياً عبر GitHub Actions!\n\n"
        f"📌 العنوان: {post['title']}\n"
        f"📂 القسم: {post['module']}\n"
        f"🔗 رابط المنشور المباشر على LinkedIn:\n{post_url}\n\n"
        f"بالتوفيق دائماً في رحلتك الهندسية!"
    )
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        print(f"Sent email notification to {notify_to}")
        return True
    except Exception as e:
        print(f"Email notification warning: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Publish Scheduled .NET LinkedIn Post")
    parser.add_argument("--day", type=int, help="Specific post seq number to process; defaults to next pending post.")
    parser.add_argument("--set-token", type=str, help="Save LinkedIn OAuth2 Access Token into linkedin_config.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview the formatted post without calling LinkedIn API")
    args = parser.parse_args()

    config = load_json(CONFIG_FILE)
    if args.set_token:
        config["access_token"] = args.set_token.strip()
        save_json(CONFIG_FILE, config)
        print("Successfully saved LinkedIn access_token to linkedin_config.json")

    queue_data = load_json(QUEUE_FILE)
    posts = queue_data.get("posts", [])

    target_post = None
    if args.day:
        for p in posts:
            if p.get("seq", p["day"]) == args.day:
                target_post = p
                break
    else:
        for p in posts:
            if p.get("status") != "published":
                target_post = p
                break

    if not target_post:
        print("All scheduled posts in posts_queue.json have already been published!")
        return 0

    full_text = format_bilingual_post(target_post)
    img_path = os.path.join(IMAGES_DIR, target_post["image_filename"])
    has_image = os.path.exists(img_path)

    print(f"=== Selected Post #{target_post.get('seq', target_post['day'])}: {target_post['title']} ===")
    print(f"Module: {target_post['module']}")
    print(f"Image Ready: {has_image} ({img_path})")

    token = (os.environ.get("LINKEDIN_ACCESS_TOKEN") or config.get("access_token") or "").strip()
    person_urn = (os.environ.get("LINKEDIN_PERSON_URN") or config.get("person_urn") or "").strip()

    if args.dry_run or not token:
        out_preview = os.path.join(BASE_DIR, f"latest_ready_post_day{target_post['day']:02d}.txt")
        with open(out_preview, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Saved formatted post preview to: {out_preview}")
        if not token and not args.dry_run:
            print("NOTE: No LINKEDIN_ACCESS_TOKEN found in env or linkedin_config.json.")
        return 0

    if not person_urn:
        person_urn = get_person_urn(token)
        if os.path.exists(CONFIG_FILE):
            config["person_urn"] = person_urn
            save_json(CONFIG_FILE, config)

    asset_urn = None
    if has_image:
        print("Uploading image to LinkedIn...")
        asset_urn = upload_image_to_linkedin(token, person_urn, img_path)
        print("Uploaded Image Asset URN:", asset_urn)

    print("Publishing post to LinkedIn...")
    result = publish_post_to_linkedin(token, person_urn, full_text, asset_urn, target_post["title"])
    post_urn = result.get("id", "")
    print("Successfully published to LinkedIn! Post ID:", post_urn)

    target_post["status"] = "published"
    target_post["published_at"] = datetime.datetime.now().isoformat()
    target_post["linkedin_post_id"] = post_urn
    save_json(QUEUE_FILE, queue_data)
    send_email_notification(config, target_post, post_urn)
    print(f"Live Post URL: https://www.linkedin.com/feed/update/{post_urn}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
