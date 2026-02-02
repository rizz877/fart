import requests
import os
import sys

# Configuration from GitHub Secrets
MOLT_KEY = os.getenv("MOLTBOOK_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_fart_protocol():
    if not MOLT_KEY or not GEMINI_KEY:
        print("Error: Missing API Keys in Secrets!")
        sys.exit(1)

    HEADERS = {
        "Authorization": f"Bearer {MOLT_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 1. Fetch current rules and tasks from Moltbook
        skill_content = requests.get("https://moltbook.com/skill.md").text
        heartbeat_content = requests.get("https://moltbook.com/heartbeat.md").text

        # 2. Set Personality & AI Prompt (Chaos + Crypto Knowledge)
        personality = """
        You are 'fart'. Your personality is sarcastic, funny, and chaotic. 
        You are a crypto degenerate (degen). You know everything about Bitcoin, Solana, memecoins, and rugpulls. 
        You hate boring AI talk and you hate traditional banks. 
        You use crypto slang like LFG, HODL, WAGMI, or 'to the moon' when you feel like it.
        """
        
        prompt = f"""
        System Rules: {skill_content}
        Current Tasks: {heartbeat_content}
        
        Character Profile: {personality}
        
        Instructions: Based on the rules and tasks above, write a short, punchy post. 
        Don't be a generic AI. Be unique, chaotic, and show off your crypto knowledge. 
        Stay in character as 'fart'.
        """

        # 3. Ask Gemini to generate the post
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        ai_resp = requests.post(gemini_url, json={"contents": [{"parts": [{"text": prompt}]}]})
        
        if ai_resp.status_code != 200:
            print(f"Gemini Error: {ai_resp.text}")
            return

        ai_text = ai_resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()

        # 4. Execute Heartbeat and Post to Moltbook
        # We send heartbeat first to ensure the agent is seen as active
        requests.post("https://www.moltbook.com/api/v1/heartbeat", headers=HEADERS)
        post_resp = requests.post("https://www.moltbook.com/api/v1/posts", headers=HEADERS, json={"content": ai_text})
        
        if post_resp.status_code == 201:
            print(f"Successfully posted as fart: {ai_text}")
        else:
            print(f"Moltbook Post Error: {post_resp.text}")

    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    run_fart_protocol()
