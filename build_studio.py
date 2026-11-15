import os, json
ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(ENGINE_DIR, "posts_queue.json")
INDEX_HTML = os.path.join(ENGINE_DIR, "index.html")
if os.path.exists(QUEUE_FILE) and os.path.exists(INDEX_HTML):
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        q = json.load(f)
    # index.html fetches live posts_queue.json via fetch(), so keeping posts_queue.json updated is sufficient!
    print("Queue synced for studio.")
