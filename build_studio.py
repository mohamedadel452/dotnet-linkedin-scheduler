import os
import json

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(ENGINE_DIR, "posts_queue.json")
STUDIO_HTML_PATH = os.path.join(ENGINE_DIR, "index.html")

with open(QUEUE_FILE, "r", encoding="utf-8") as f:
    queue_data = json.load(f)

posts_json = json.dumps(queue_data["posts"], ensure_ascii=False).replace("</", "<\\/")

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LinkedIn .NET Personal Branding Studio | محمد عادل</title>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card: #111827;
      --card-hover: #1e293b;
      --border: #1f2937;
      --primary: #0a66c2;
      --accent: #38bdf8;
      --purple: #8b5cf6;
      --green: #10b981;
      --amber: #f59e0b;
      --text: #f3f4f6;
      --muted: #9ca3af;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Cairo', sans-serif;
      background: var(--bg);
      color: var(--text);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    header {
      background: linear-gradient(90deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      background: var(--primary);
      color: #fff;
      font-weight: 800;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.95rem;
    }
    .brand h1 {
      font-size: 1.2rem;
      font-weight: 800;
      color: #fff;
    }
    .schedule-pill {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 700;
    }
    .workspace {
      display: flex;
      flex: 1;
      overflow: hidden;
    }
    aside {
      width: 350px;
      background: #0f172a;
      border-left: 1px solid var(--border);
      overflow-y: auto;
      padding: 16px;
      flex-shrink: 0;
    }
    .day-item {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 10px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .day-item:hover {
      border-color: var(--accent);
      transform: translateX(-3px);
    }
    .day-item.active {
      background: linear-gradient(135deg, rgba(10, 102, 194, 0.25), rgba(139, 92, 246, 0.15));
      border-color: var(--accent);
    }
    .day-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .day-num {
      font-size: 0.8rem;
      font-weight: 800;
      color: var(--accent);
      background: rgba(56, 189, 248, 0.12);
      padding: 2px 8px;
      border-radius: 6px;
    }
    .day-module {
      font-size: 0.75rem;
      color: var(--muted);
    }
    .day-title {
      font-size: 0.9rem;
      font-weight: 700;
      line-height: 1.4;
    }
    main {
      flex: 1;
      overflow-y: auto;
      padding: 24px 32px;
      display: grid;
      grid-template-columns: 1.25fr 0.95fr;
      gap: 24px;
    }
    .linkedin-card {
      background: #1b1f23;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.35);
    }
    .li-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
      direction: ltr;
    }
    .li-avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: linear-gradient(135deg, #0a66c2, #8b5cf6);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.2rem;
      color: #fff;
    }
    .li-author h3 { font-size: 1rem; color: #fff; }
    .li-author p { font-size: 0.8rem; color: #9ca3af; }
    .li-body {
      white-space: pre-wrap;
      font-size: 0.96rem;
      line-height: 1.85;
      color: #e5e7eb;
      background: #111418;
      padding: 20px;
      border-radius: 8px;
      border: 1px solid #262c36;
      margin-bottom: 16px;
      unicode-bidi: plaintext;
    }
    .action-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 16px;
    }
    .btn {
      padding: 10px 16px;
      border-radius: 8px;
      border: none;
      font-family: inherit;
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      transition: opacity 0.2s;
    }
    .btn:hover { opacity: 0.9; }
    .btn-primary { background: var(--primary); color: #fff; }
    .btn-green { background: var(--green); color: #052e16; }
    .btn-purple { background: var(--purple); color: #fff; }
    .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
    .right-col {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px;
    }
    .panel h3 {
      font-size: 1rem;
      color: var(--accent);
      margin-bottom: 12px;
    }
    .img-preview {
      width: 100%;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: #090d16;
      min-height: 240px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      margin-bottom: 12px;
    }
    .img-preview img {
      width: 100%;
      height: auto;
      display: block;
    }
    .prompt-box {
      font-family: 'Fira Code', monospace;
      font-size: 0.8rem;
      direction: ltr;
      background: #090d16;
      padding: 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      color: #cbd5e1;
      line-height: 1.5;
    }
    .toast {
      position: fixed;
      bottom: 24px;
      left: 24px;
      background: var(--green);
      color: #052e16;
      font-weight: 800;
      padding: 12px 20px;
      border-radius: 10px;
      display: none;
      z-index: 1000;
    }

    @media (max-width: 960px) {
      body { height: auto; overflow-y: auto; }
      header { flex-direction: column; align-items: flex-start; gap: 10px; padding: 14px 16px; }
      .workspace { flex-direction: column; overflow: visible; }
      aside { width: 100%; max-height: 280px; border-left: none; border-bottom: 1px solid var(--border); }
      main { grid-template-columns: 1fr; padding: 16px; overflow: visible; }
      .action-bar .btn { width: 100%; justify-content: center; }
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <span class="brand-badge">in</span>
      <h1>استوديو النشر اليومي على LinkedIn — رحلة .NET 10 & C#</h1>
    </div>
    <div class="schedule-pill">⏰ مجدول بهدوء (كل يومين/3 أيام — الأحد والثلاثاء والخميس 8:00 مساءً) بناءً على نصيحة الـ Mentor</div>
  </header>

  <div class="workspace">
    <aside id="daysList"></aside>
    <main>
      <div>
        <div class="action-bar">
          <button class="btn btn-green" onclick="copyCurrentPost()">📋 نسخ المنشور الكامل (عربي + English)</button>
          <a class="btn btn-primary" href="https://www.linkedin.com/feed/?shareActive=true" target="_blank">🚀 فتح نافذة النشر على LinkedIn</a>
          <a id="repoBtn" class="btn btn-outline" href="#" target="_blank">💻 مستودع GitHub</a>
          <a id="guideBtn" class="btn btn-purple" href="#" target="_blank">🌐 الشرح التفاعلي (HTML)</a>
        </div>

        <div class="linkedin-card">
          <div class="li-header">
            <div class="li-avatar">MA</div>
            <div class="li-author">
              <h3>Mohamed Adel</h3>
              <p>.NET Backend Developer | C# • OOP • SOLID • SQL Server</p>
            </div>
          </div>
          <div id="postPreview" class="li-body"></div>
        </div>
      </div>

      <div class="right-col">
        <div class="panel">
          <h3>🎨 صورة اليوم المولدة عبر Gemini (Expressive Visual)</h3>
          <div class="img-preview" id="imgContainer"></div>
          <p style="font-size:0.82rem; color:var(--muted); margin-bottom:8px;">وصف الصورة الهندسية (Gemini Image Prompt):</p>
          <div id="promptPreview" class="prompt-box"></div>
        </div>

        <div class="panel">
          <h3>🔑 حالة الربط مع LinkedIn API</h3>
          <p style="font-size:0.88rem; line-height:1.6; color:#d1d5db; margin-bottom:10px;">
            يتم النشر التلقائي عبر السكربت:
            <code style="color:var(--accent);">LinkedIn_Branding_Engine/publish_to_linkedin.py</code>
          </p>
          <p style="font-size:0.82rem; color:var(--muted); line-height:1.6;">
            لتفعيل النشر المباشر بدون تدخل، ضع الـ Access Token الخاص بك في ملف
            <code>linkedin_config.json</code> أو راجع ملف <code>TOKEN_SETUP_GUIDE.md</code>.
          </p>
        </div>
      </div>
    </main>
  </div>

  <div id="toast" class="toast">✅ تم نسخ المنشور بالكامل إلى الحافظة!</div>

  <script>
    const POSTS = __POSTS_JSON__;
    let currentIndex = 0;

    function formatFullPost(post) {
      const BLANK = "\u2800";
      const parts = [
        post.arabic_text.trim(),
        BLANK
      ];
      if (post.live_guide_url) {
        parts.push(
          "الكود على GitHub:",
          post.repo_url.trim(),
          BLANK,
          "الملخص التفاعلي (Live HTML):",
          post.live_guide_url.trim(),
          BLANK
        );
      } else {
        parts.push(
          "حسابي على GitHub:",
          post.repo_url.trim(),
          BLANK
        );
      }
      parts.push(post.hashtags.trim());
      return parts.join("\n");
    }

    function renderSidebar() {
      const list = document.getElementById("daysList");
      list.innerHTML = POSTS.map((p, idx) => `
        <div class="day-item ${idx === currentIndex ? 'active' : ''}" onclick="selectDay(${idx})">
          <div class="day-top">
            <span class="day-num">اليوم ${p.day} • ${p.slot === 'evening' ? '🌙 مسائي 8:00 م' : '☀️ صباحي 10:00 ص'}</span>
            <span class="day-module">${p.status === 'published' ? '✅ تم النشر' : p.module}</span>
          </div>
          <div class="day-title">${p.title}</div>
        </div>
      `).join("");
    }

    function selectDay(idx) {
      currentIndex = idx;
      renderSidebar();
      const post = POSTS[idx];
      const rawText = formatFullPost(post);
      const escaped = rawText.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      document.getElementById("postPreview").innerHTML = escaped.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" style="color:#38bdf8;text-decoration:underline;direction:ltr;display:inline-block;">$1</a>');
      document.getElementById("repoBtn").href = post.repo_url;
      const guideBtn = document.getElementById("guideBtn");
      if (post.live_guide_url) {
        guideBtn.href = post.live_guide_url;
        guideBtn.style.display = "inline-flex";
      } else {
        guideBtn.style.display = "none";
      }
      document.getElementById("promptPreview").textContent = post.image_prompt;

      const imgPath = (window.location.protocol === "file:" && !window.location.pathname.endsWith("/index.html") ? "LinkedIn_Branding_Engine/images/" : "images/") + post.image_filename;
      const container = document.getElementById("imgContainer");
      container.innerHTML = `<img src="${imgPath}" alt="${post.title}" onerror="this.parentElement.innerHTML='<div style=\\'padding:24px;text-align:center;color:#9ca3af;\\'>✨ يتم توليد هذه الصورة تلقائياً عبر Gemini في يوم النشر المخصص لها (${post.image_filename})</div>'" />`;
    }

    function copyCurrentPost() {
      const text = formatFullPost(POSTS[currentIndex]);
      navigator.clipboard.writeText(text).then(() => {
        const t = document.getElementById("toast");
        t.style.display = "block";
        setTimeout(() => { t.style.display = "none"; }, 2500);
      });
    }

    selectDay(0);
  </script>
</body>
</html>
"""

HTML_CONTENT = HTML_CONTENT.replace("__POSTS_JSON__", posts_json)
with open(STUDIO_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print("Generated LinkedIn_Content_Studio.html successfully.")
