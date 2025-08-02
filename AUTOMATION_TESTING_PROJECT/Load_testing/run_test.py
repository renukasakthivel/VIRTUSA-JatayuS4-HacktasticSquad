import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

locust_dir = "locust_scripts"
report_dir = "locust_reports"
log_file = os.path.join("logs", "failed_hosts.txt")

os.makedirs(report_dir, exist_ok=True)
os.makedirs("logs", exist_ok=True)

def run_locust_test(script_file):
    host_name = script_file.split("locustfile_")[1].split(".py")[0]
    host_url = host_name.replace("_", ".")
    report_path = os.path.join(report_dir, host_name)
    os.makedirs(report_path, exist_ok=True)

    print(f"\n🚀 Running load test for: {host_url}...")

    cmd = [
        "locust",
        "-f", os.path.join(locust_dir, script_file),
        "--headless",
        "-u", "10", "-r", "5", "-t", "10s",
        "--host", f"https://{host_url}",
        "--html", os.path.join(report_path, "report.html"),
        "--csv", os.path.join(report_path, "report")
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Load test failed for {host_name}")
        with open(log_file, "a") as f:
            f.write(f"{host_name}\n")

def main():
    scripts = [f for f in os.listdir(locust_dir) if f.endswith(".py")]

    if not scripts:
        print("⚠️ No locust scripts found in locust_scripts/")
        return

    with ThreadPoolExecutor() as executor:
        executor.map(run_locust_test, scripts)

    print("\n📁 All tests complete. Reports stored in locust_reports/")

if __name__ == "__main__":
    main()
