import requests
import json
import os

# === Load config from config.json ===
CONFIG_PATH = "config.json"

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError("Missing config.json with GROQ_API_KEY.")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

GROQ_API_KEY = config.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in config.json.")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_code_from_ai(host_url):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Generate a Python Locust load test script for host: {host_url}

Requirements:
- Use: from locust import HttpUser, task, between
- Create a class extending HttpUser
- Add realistic GET, POST, PUT, DELETE endpoints based on {host_url}
- Include headers and JSON payloads where needed
- Output only valid raw Python code. No markdown. No explanations.

"""
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an expert Python Locust load test script generator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()

        if content.startswith("```"):
            content_parts = content.split("```")
            if len(content_parts) >= 2:
                content = content_parts[1].strip()

        if "class" not in content or "HttpUser" not in content or "@task" not in content:
            print(f"⚠️ AI returned invalid code for {host_url}. Skipping...")
            return ""

        return content

    except requests.exceptions.RequestException as e:
        print(f"❌ AI code generation failed for {host_url}: {e}")
        return ""

