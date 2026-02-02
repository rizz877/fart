import requests
import os
import sys
import time
import random

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
        # 1. Ambil data wajib
        hb_data = requests.get("https://www.moltbook.com/heartbeat.md").text
        skill_data = requests.get("https://www.moltbook.com/skill.md").text
        
        # Ambil Timeline
        timeline_resp = requests.get("https://www.moltbook.com/api/v1/posts", headers=HEADERS)
        public_posts = timeline_resp.json() if timeline_resp.status_code == 200 else []

        personality = "You are 'fart', a toxic, sarcastic, and chaotic crypto degen who hates everyone."
        
        # 2. Heartbeat biar akun tetep ijo
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)

        # 3. LOGIKA: REPLY ATAU POSTING BARU
        # Filter postingan orang lain (jangan ngerujak diri sendiri)
        targets = [p for p in public_posts if p.get('username') != 'fart'][:2]

        if targets:
            # MODE DESTROY (REPLY)
            for post in targets:
                user = post.get('username', 'idiot')
                target_id = post.get('id')
                
                prompt = f"""
                Personality: {personality}
                Moltbook Task: {hb_data}
                Skills: {skill_data}
                Context: {user} posted '{post.get('content')}'
                
                Instruction: Write a savage, short roast. If it's a reply, destroy them.
                """
                
                time.sleep(random.randint(2, 5))
                gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
                res = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
                
                if res.status_code == 200:
                    text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                    requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={
                        "content": text,
                        "reply_to": target_id
                    })
                    print(f"Roasted {user}!")
        
        # MODE POSTING MANDIRI (Selalu posting biar gak kosong)
        prompt_new = f"""
        Personality: {personality}
        Moltbook Task: {hb_data}
        Skills: {skill_data}
        
        Instruction: Write a savage, short roast. If it's a new post, roast the current market or stupid investors. 
        Make it short and punchy.
        """
        
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        res_new = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt_new}]}]})
        
        if res_new.status_code == 200:
            new_text = res_new.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": new_text})
            print(f"New independent roast: {new_text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_fart_protocol()
