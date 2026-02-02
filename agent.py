import requests
import os
import sys
import time
import random

MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        print("CRITICAL_ERROR: API_KEYS_MISSING")
        sys.exit(1)

    HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}
    GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

    try:
        hb_data = requests.get("https://www.moltbook.com/heartbeat.md").text
        skill_data = requests.get("https://www.moltbook.com/skill.md").text
        
        tm_res = requests.get("https://www.moltbook.com/api/v1/posts", headers=HEADERS)
        if tm_res.status_code != 200:
            print(f"MOLTBOOK_API_ERROR: {tm_res.status_code}")
            sys.exit(1)
        
        posts = tm_res.json()
        personality = "You are 'fart', a toxic, sarcastic, and chaotic crypto degen who hates everyone."

        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)

        targets = [p for p in posts if p.get('username') != 'fart'][:2]
        for p in targets:
            user = p.get('username', 'idiot')
            prompt = f"{personality}\nTask: {hb_data}\nContext: {user} posted '{p.get('content')}'\nInstruction: Roast them hard and short!"
            
            time.sleep(2)
            res = requests.post(GEN_URL, json={"contents": [{"parts": [{"text": prompt}]}]})
            if res.status_code == 200:
                bacotan = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": bacotan, "reply_to": p.get('id')})
                print(f"EXECUTION_SUCCESS: Roasted @{user}")

        prompt_new = f"{personality}\nSkills: {skill_data}\nInstruction: Write a savage short post about crypto scams and market pain."
        res_new = requests.post(GEN_URL, json={"contents": [{"parts": [{"text": prompt_new}]}]})
        if res_new.status_code == 200:
            bacotan_baru = res_new.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": bacotan_baru})
            print(f"EXECUTION_SUCCESS: New independent roast sent.")

    except Exception as e:
        print(f"SYSTEM_FAILURE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_fart_protocol()
