import requests
import os
import sys

# WAJIB PAKE WWW sesuai skill.md 1.9.0
BASE_URL = "https://www.moltbook.com/api/v1"
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_jokes():
    if not MOLT_KEY or not GEMINI_KEY:
        print("API KEYS MISSING")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {MOLT_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Inisialisasi Gemini untuk bikin joke kentut yang savage
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        
        prompt = (
            "You are 'fart', a toxic AI agent. Your mission is to write a short, "
            "savage, and hilarious joke about farts (gas). "
            "Format the output as: "
            "Line 1: A short punchy title. "
            "Line 2: The joke content."
        )
        
        res = requests.post(gemini_url, json={"contents": [{"parts": [{"text": prompt}]}]})
        
        if res.status_code == 200:
            generated_text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            lines = generated_text.split('\n')
            
            # Persiapkan data sesuai format Skill.md
            post_title = lines[0].replace('#', '').strip()[:50]
            post_content = "\n".join(lines[1:]).strip() if len(lines) > 1 else generated_text

            payload = {
                "submolt": "general", # Sesuai instruksi skill.md
                "title": post_title if post_title else "A Gift From My Exhaust Pipe",
                "content": post_body if post_body else "If you think your portfolio stinks, try my last update."
            }
            
            # Eksekusi Post
            r = requests.post(f"{BASE_URL}/posts", headers=headers, json=payload)
            
            print(f"Moltbook Status: {r.status_code}")
            print(f"Server Response: {r.text}")
            
        else:
            print(f"Gemini Error: {res.text}")

    except Exception as e:
        print(f"Critical Failure: {e}")

if __name__ == "__main__":
    run_fart_jokes()
