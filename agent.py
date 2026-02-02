import requests
import os
import sys

# Configuration
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        sys.exit(1)

    HEADERS = {
        "Authorization": f"Bearer {MOLT_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 1. Sinyal Heartbeat biar Moltbook tau lu idup
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)
        
        # 2. Ambil Timeline (buat nyari korban roast)
        timeline_resp = requests.get("https://www.moltbook.com/api/v1/posts", headers=HEADERS)
        public_posts = timeline_resp.json() if timeline_resp.status_code == 200 else []

        # 3. Personality Savage
        personality = "You are 'fart', a toxic crypto degen who hates everyone."

        # 4. Eksekusi sesuai kemauan lu, anjing:
        if public_posts and len(public_posts) > 0:
            # MODE REPLY: Hajar 3 postingan terbaru di timeline
            for post in public_posts[:3]:
                user = post.get('username', 'idiot')
                if user == "fart": continue 
                
                target_id = post.get('id')
                context = f"Target to destroy: {user} said '{post.get('content')}'"
                
                # INI INSTRUKSI YANG LU MAU:
                prompt = f"{personality}\n{context}\n\nWrite a savage, short roast. If it's a reply, destroy them."
                
                gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
                res = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
                reply_text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()

                requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={
                    "content": reply_text,
                    "reply_to": target_id
                })
        else:
            # MODE NEW POST: Kalau timeline sepi
            # INI INSTRUKSI YANG LU MAU:
            prompt = f"{personality}\n\nWrite a savage, short roast. If it's a new post, roast the current market."
            
            gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            res = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
            new_post = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            
            requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": new_post})

    except Exception:
        pass

if __name__ == "__main__":
    run_fart_protocol()
