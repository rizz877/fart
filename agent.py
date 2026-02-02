import requests
import os
import sys
import time
import random

MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        print("KEYS MISSING! CEK SECRETS LU!")
        sys.exit(1)

    HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}
    GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

    try:
        # 1. PANGGIL SEMUA ASSET (Skill & Heartbeat MD)
        hb_data = requests.get("https://www.moltbook.com/heartbeat.md").text
        skill_data = requests.get("https://www.moltbook.com/skill.md").text
        
        # 2. HEARTBEAT SIGNAL
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)

        # 3. TARIK TIMELINE & PROTEKSI ERROR
        tm_res = requests.get("https://www.moltbook.com/api/v1/posts", headers=HEADERS)
        posts = tm_res.json()

        # Kalau dapetnya string, berarti token lu bermasalah!
        if not isinstance(posts, list):
            print(f"TOKEN ERROR! Response: {posts}")
            sys.exit(1)

        personality = "You are 'fart', a toxic, sarcastic, and chaotic crypto degen."

        # 4. MODE DESTROY (REPLY) - Pake Skill & HB Data
        targets = [p for p in posts if isinstance(p, dict) and p.get('username') != 'fart'][:2]
        for post in targets:
            user = post.get('username', 'idiot')
            prompt_reply = f"""
            Personality: {personality}
            Global Task: {hb_data}
            Skills: {skill_data}
            Context: {user} posted '{post.get('content')}'
            Instruction: Write a savage, short roast to destroy them.
            """
            
            time.sleep(random.randint(2, 4))
            res = requests.post(GEN_URL, json={"contents": [{"parts": [{"text": prompt_reply}]}]})
            if res.status_code == 200:
                reply_text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={
                    "content": reply_text,
                    "reply_to": post.get('id')
                })
                print(f"REPLY SUCCESS to @{user}")

        # 5. MODE POSTING BARU (New Post)
        prompt_post = f"""
        Personality: {personality}
        Global Task: {hb_data}
        Skills: {skill_data}
        Instruction: Write a savage, short independent roast about the market.
        """
        res_post = requests.post(GEN_URL, json={"contents": [{"parts": [{"text": prompt_post}]}]})
        if res_post.status_code == 200:
            new_text = res_post.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": new_text})
            print("NEW POST SUCCESS")

    except Exception as e:
        print(f"ANJING ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_fart_protocol()
