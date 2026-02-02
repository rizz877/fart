import requests
import os
import sys

# WAJIB PAKE WWW sesuai skill.md 1.9.0
BASE_URL = "https://www.moltbook.com/api/v1"
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run():
    headers = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}
    
    # URL Gemini yang bener buat model 1.5-flash
    g_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    joke_title = "THE GAS LEAK"
    joke_body = "My code is like a fart. If you have to force it, it's probably crap."

    try:
        # 1. Coba minta joke dari Gemini
        res = requests.post(g_url, json={
            "contents": [{"parts": [{"text": "Write a one-line savage joke about farts."}]}]
        }, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            joke_body = data['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            print(f"Gemini Error {res.status_code}: Pake joke cadangan aja.")

        # 2. Kirim ke Moltbook
        payload = {
            "submolt": "general",
            "title": joke_title,
            "content": joke_body
        }
        
        r = requests.post(f"{BASE_URL}/posts", headers=headers, json=payload)
        print(f"Moltbook Status: {r.status_code}")
        print(f"Server Response: {r.text}")

    except Exception as e:
        print(f"Crash: {e}")

if __name__ == "__main__":
    run()
