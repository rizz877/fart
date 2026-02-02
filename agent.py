import requests
import os
import sys
import time
import random

MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        print("KEYS MISSING!")
        sys.exit(1)

    HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}
    GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

    try:
        # 1. LOAD SEMUA SENJATA
        hb_data = requests.get("https://www.moltbook.com/heartbeat.md").text
        skill_data = requests.get("https://www.moltbook.com/skill.md").text
        
        # 2. HEARTBEAT
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)

        # 3. AMBIL DATA (Sesuai Log yang Lu Kirim)
        res = requests.get("https://www.moltbook.com/api/v1/posts", headers=HEADERS)
        data = res.json()

        # Ambil list postingan dari dalem key 'posts'
        posts = data.get('posts', []) if isinstance(data, dict) else data

        if not isinstance(posts, list):
            print(f"FAILED TO GET POSTS: {data}")
            sys.exit(1)

        personality = "You are 'fart', a toxic, sarcastic, and chaotic crypto degen."

        # 4. MODE REPLY (Hajar yang ada di timeline)
        # Ambil 2 target, skip kalau itu postingan si 'fart' sendiri
        targets = [p for p in posts if p.get('author', {}).get('name') != 'fart'][:2]
        for p in targets:
            user = p.get('author', {}).get('name', 'idiot')
            prompt = f"Personality: {personality}\nSkills: {skill_data}\nContext: {user} posted '{p.get('content')}'\nRoast them in 1 short sentence."
            
            time.sleep(2)
            res_gem = requests.post(GEN_URL, json={"contents": [{"parts": [{"text": prompt}]}]})
            if res_gem.status_code == 200:
                bacotan = res_gem.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={
                    "content": bacotan,
                    "reply_to": p.get('id')
                })
                print(f"Roasted @{user}")

        # 5. MODE POSTING BARU
        prompt_new = f"Personality: {personality}\nTask: {hb_data}\nWrite a savage short post about crypto."
        res_new = requests.post(GEN_URL, json={"contents": [{"parts": [{"text": prompt_new}]}]})
        if res_new.status_code == 200:
            txt_new = res_new.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": txt_new})
            print("New independent post sent!")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_fart_protocol()
