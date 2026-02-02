import requests
import os
import sys
import time
import random

# API Keys
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    # Cek Key (Jangan sampe kosong babi)
    if not MOLT_KEY or not GEMINI_KEY:
        print("ERROR: Key lu kaga ada di GitHub Secrets, anjing!")
        sys.exit(1)

    HEADERS = {
        "Authorization": f"Bearer {MOLT_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 1. Ambil Nyawa Agent
        hb_data = requests.get("https://www.moltbook.com/heartbeat.md").text
        skill_data = requests.get("https://www.moltbook.com/skill.md").text
        
        # 2. Ambil Timeline korban
        timeline_resp = requests.get("https://www.moltbook.com/api/v1/posts", headers=HEADERS)
        if timeline_resp.status_code != 200:
            print(f"ERROR MOLTBOOK API: {timeline_resp.status_code} - {timeline_resp.text}")
            sys.exit(1)
            
        public_posts = timeline_resp.json()

        personality = "You are 'fart', a toxic, sarcastic, and chaotic crypto degen who hates everyone."
        
        # 3. Sinyal Idup
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)

        # 4. MODE REPOST/REPLY (Destroy Mode)
        targets = [p for p in public_posts if p.get('username') != 'fart'][:2]
        if targets:
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
                    post_res = requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={
                        "content": text,
                        "reply_to": target_id
                    })
                    print(f"SUCCESS: Roasted {user} with: {text}")
                else:
                    print(f"GEMINI ERROR: {res.text}")

        # 5. MODE NEW POST (Maksa Posting Biar Kaga Kosong)
        prompt_new = f"""
        Personality: {personality}
        Moltbook Task: {hb_data}
        Skills: {skill_data}
        
        Instruction: Write a savage, short roast. If it's a new post, roast the current market.
        """
        
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        res_new = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt_new}]}]})
        
        if res_new.status_code == 200:
            new_text = res_new.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": new_text})
            print(f"SUCCESS: New independent roast: {new_text}")

    except Exception as e:
        print(f"ANJING ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_fart_protocol()
