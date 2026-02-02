import requests
import os
import sys

# WAJIB PAKE WWW!
BASE_URL = "https://www.moltbook.com/api/v1"
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run():
    if not MOLT_KEY or not GEMINI_KEY:
        print("KEYS KOSONG, CEK SECRETS!")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}

    try:
        # 1. Ambil skill biar AI pinteran dikit
        skill_res = requests.get("https://www.moltbook.com/skill.md")
        skill_text = skill_res.text if skill_res.status_code == 200 else "Always use www"

        # 2. Panggil Gemini V1 (Stable)
        g_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        prompt = f"Skill: {skill_text}\nPersona: 'fart', a toxic AI. Write a savage one-line fart joke. Line 1: Title, Line 2: Joke."

        res = requests.post(g_url, json={"contents": [{"parts": [{"text": prompt}]}]})
        
        if res.status_code == 200:
            raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            lines = raw.split('\n')
            
            # 3. Post ke Moltbook
            payload = {
                "submolt": "general", # Key sesuai skill.md
                "title": lines[0].replace('#', '').strip()[:50],
                "content": "\n".join(lines[1:]).strip() if len(lines) > 1 else raw
            }
            
            r = requests.post(f"{BASE_URL}/posts", headers=headers, json=payload)
            print(f"Moltbook Status: {r.status_code}")
            print(f"Response: {r.text}")
        else:
            print(f"Gemini Error: {res.text}")

    except Exception as e:
        print(f"Crash: {e}")

if __name__ == "__main__":
    run()
