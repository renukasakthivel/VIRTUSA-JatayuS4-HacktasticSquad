import os
from urllib.parse import urlparse
from ai_generator import generate_code_from_ai

host_urls = [
    "https://dummyjson.com",
    "https://fakestoreapi.com",
    "https://fakeapi.net"
]

os.makedirs("locust_scripts", exist_ok=True)

for url in host_urls:
    parsed = urlparse(url)
    safe_name = parsed.netloc.replace(".", "_")
    filename = f"locustfile_{safe_name}.py"
    filepath = os.path.join("locust_scripts", filename)

    print(f"🧠 Generating Locust script for {url}")
    code = generate_code_from_ai(url)

    if code:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"✅ Saved: {filepath}")
    else:
        print(f"⚠️ Skipped: {url}")
