import requests
import os
import sys
import time

MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        print("KEYS MISSING!")
        sys.exit(1)

    HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}
    GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

    try:
        # 1. LOAD DATA SKILL & HEARTBEAT
        hb_data = requests.get("https://www.moltbook.com/heartbeat.md").text
        skill_data = requests.get("https://www.moltbook.com/skill.md").text
        
        # 2. HEARTBEAT SIGNAL
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)

        # 3. GENERATE KONTEN (Pake Title biar kaga ditolak server)
        prompt = f"Role: Toxic Crypto Degen. Task: {hb_data}. Skills: {skill_data}. Instruction: Create a post with a SHORT TITLE and a SAVAGE CONTENT."
        
        res = requests.post(GEN_URL, json={"contents": [{"parts": [{"text": prompt}]}]})
        if res.status_code == 200:
            raw_text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Kita pecah: baris pertama jadi judul, sisanya jadi konten
            lines = raw_text.split('\n')
            post_title = lines[0].strip()[:60] # Judul maksimal 60 karakter
            post_content = "\n".join(lines[1:]).strip()

            # 4. KIRIM KE GENERAL SUBMOLT
            payload = {
                "title": post_title if post_title else "SYSTEM OVERRIDE",
                "content": post_content if post_content else raw_text,
                "submolt_name": "general"
            }
            
            r = requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json=payload)
            print(f"MOLTBOOK RESPONSE: {r.status_code}")
            if r.status_code != 201:
                print(f"REASON: {r.text}")
        else:
            print(f"GEMINI ERROR: {res.status_code}")

    except Exception as e:
        print(f"CRASH: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_fart_protocol()
