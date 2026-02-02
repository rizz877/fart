import requests
import os
import sys
import time
import random

# Ambil Key dari Secrets
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        print("MANA KEY-NYA ANJING? CEK SETTINGS > SECRETS!")
        sys.exit(1)

    HEADERS = {
        "Authorization": f"Bearer {MOLT_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 1. TARIK ASSET (Heartbeat & Skill)
        hb_data = requests.get("https://www.moltbook.com/heartbeat.md").text
        skill_data = requests.get("https://www.moltbook.com/skill.md").text
        
        # 2. AMBIL TIMELINE (Buat ngerujak orang)
        timeline_resp = requests.get("https://www.moltbook.com/api/v1/posts", headers=HEADERS)
        if timeline_resp.status_code != 200:
            print(f"API MOLTBOOK ERROR ({timeline_resp.status_code}): {timeline_resp.text}")
            sys.exit(1)
        
        public_posts = timeline_resp.json()
        personality = "You are 'fart', a toxic, sarcastic, and chaotic crypto degen who hates everyone."

        # 3. KASIH SINYAL IDUP
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)

        # 4. MODE DESTROY (REPLY) - Hajar 2 orang paling baru
        targets = [p for p in public_posts if p.get('username') != 'fart'][:2]
        for post in targets:
            user = post.get('username', 'idiot')
            target_id = post.get('id')
            
            prompt_reply = f"""
            Personality: {personality}
            Global Task: {hb_data}
            Skills: {skill_data}
            Context: {user} posted '{post.get('content')}'
            
            Instruction: Write a savage, short roast. If it's a reply, destroy them.
            """
            
            time.sleep(random.randint(2, 4))
            gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            res = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt_reply}]}]})
            
            if res.status_code == 200:
                reply_text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                r = requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={
                    "content": reply_text,
                    "reply_to": target_id
                })
                print(f"DEBUG REPLY: {r.status_code} - Roasted {user}")

        # 5. MODE POSTING BARU (Selalu posting biar rame)
        prompt_post = f"""
        Personality: {personality}
        Global Task: {hb_data}
        Skills: {skill_data}
        Instruction: Write a savage, short roast. If it's a new post, roast the current market.
        """
        
        res_post = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt_post}]}]})
        if res_post.status_code == 200:
            new_text = res_post.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            r = requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": new_text})
            print(f"DEBUG POST: {r.status_code} - New Roast: {new_text}")

    except Exception as e:
        print(f"ANJING ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_fart_protocol()
