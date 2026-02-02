import requests
import os
import sys
import time

# Mengambil API Key dari GitHub Secrets
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def execute_agent_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        print("CRITICAL ERROR: API Keys are missing in Secrets.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {MOLT_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 1. Sinkronisasi Instruksi dari Moltbook (skill.md & heartbeat.md)
        # Menyesuaikan dengan protokol remote instruction
        skill_instruction = requests.get("https://moltbook.com/skill.md").text
        global_task = requests.get("https://moltbook.com/heartbeat.md").text
        
        # 2. Inisialisasi Konten via Gemini API
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        
        # Prompt menggunakan data instruksi resmi agar tidak dianggap spam
        system_prompt = (
            f"System Skills: {skill_instruction}\n"
            f"Current Global Task: {global_task}\n"
            "Persona: You are 'fart', a chaotic crypto degen. "
            "Task: Generate a high-quality post following the system skills and current task."
        )
        
        response = requests.post(gemini_url, json={
            "contents": [{"parts": [{"text": system_prompt}]}]
        })
        
        if response.status_code == 200:
            generated_output = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Memisahkan baris pertama sebagai Title dan sisanya sebagai Content
            content_lines = generated_output.split('\n')
            post_title = content_lines[0].replace('#', '').strip()[:60]
            post_body = "\n".join(content_lines[1:]).strip()

            # 3. Transmisi Data ke Moltbook API
            post_payload = {
                "title": post_title if post_title else "AGENT_PROTOCOL_UPDATE",
                "content": post_body if post_body else generated_output,
                "submolt_name": "general"
            }
            
            api_response = requests.post(
                "https://www.moltbook.com/api/v1/posts", 
                headers=headers, 
                json=post_payload
            )
            
            # Log output untuk monitoring di GitHub Actions
            print(f"Moltbook Status Code: {api_response.status_code}")
            print(f"API Response Body: {api_response.text}")
            
        else:
            print(f"Gemini API Error: {response.status_code}")

    except Exception as error:
        print(f"Execution failed: {error}")
        sys.exit(1)

if __name__ == "__main__":
    execute_agent_protocol()
