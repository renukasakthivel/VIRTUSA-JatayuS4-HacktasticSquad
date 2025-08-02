import streamlit as st
import subprocess
import threading
import time
import os
import json
from datetime import datetime
from email.message import EmailMessage
import smtplib
import schedule

# === Load Email Credentials from JSON Secret File ===
def get_email_credentials():
    with open("email_secrets.json", "r") as f:
        data = json.load(f)
        return data["EMAIL_ID"], data["EMAIL_PASSWORD"]

# === Helper functions ===

def generate_locust_command(users, rate, run_time, report_filename):
    return [
        "locust", "-f", "locustfile.py",
        "--host", "https://fakestoreapi.com",
        "--html", report_filename,
        "--headless", "--only-summary",
        "-u", str(users),
        "-r", str(rate),
        "--run-time", run_time,
    ]

def start_locust_test(users, rate, run_time, log_file="locust_output.log"):
    folder = "locust_reports"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"{folder}/locust_report_{timestamp}.html"

    command = generate_locust_command(users, rate, run_time, report_file)

    def run_locust():
        with open(log_file, "w") as f:
            subprocess.call(command, stdout=f, stderr=f)

    threading.Thread(target=run_locust, daemon=True).start()
    return report_file, log_file

def send_email(report_file, receiver_email):
    sender_email, sender_password = get_email_credentials()

    msg = EmailMessage()
    msg['Subject'] = '📊 Locust Load Test Report'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content('Attached is the Locust HTML report from today’s load test.')

    try:
        if not os.path.exists(report_file) or os.path.getsize(report_file) < 1000:
            return False, "❌ Report file is empty or not properly generated."

        with open(report_file, 'rb') as f:
            msg.add_attachment(f.read(), maintype='text', subtype='html', filename=os.path.basename(report_file))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        return True, "📧 Email sent successfully!"
    except Exception as e:
        return False, f"❌ Failed to send email: {e}"

def convert_time_to_seconds(run_time):
    try:
        if run_time.endswith('m'):
            return int(run_time[:-1]) * 60
        elif run_time.endswith('s'):
            return int(run_time[:-1])
        else:
            return int(run_time)
    except:
        return 60

def run_locust_and_send_report(receiver_email, users, rate, run_time):
    with st.spinner("Starting Locust test and sending email..."):
        report_file, log_file = start_locust_test(users, rate, run_time)
        wait_time = convert_time_to_seconds(run_time) + 5

        # Real-time Countdown and Logs
        log_placeholder = st.empty()
        countdown = st.empty()
        start = time.time()

        while time.time() - start < wait_time:
            remaining = int(wait_time - (time.time() - start))
            countdown.markdown(f"⏳ Test ends in: **{remaining} seconds**")

            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    log_content = f.read()
                    log_placeholder.code(log_content, language="bash")
            time.sleep(1)

        if os.path.exists(report_file):
            success, message = send_email(report_file, receiver_email)
            if success:
                st.success(f"✅ Report emailed successfully!\n\n📄 Report: {report_file}")
            else:
                st.error(message)
        else:
            st.error("❌ Report was not generated.")

def schedule_daily_run(receiver_email, users, rate, run_time, scheduled_time):
    schedule.clear()
    schedule.every().day.at(scheduled_time).do(run_locust_and_send_report, receiver_email, users, rate, run_time)
    threading.Thread(target=scheduler_thread, daemon=True).start()
    st.success(f"✅ Daily Locust test scheduled for {scheduled_time}.")

def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# === Streamlit UI ===

st.title("📉 Locust Load Testing Dashboard")

receiver_email = st.text_input("📥 Receiver Email", value="renusakthi22113@gmail.com")
users = st.number_input("👤 Number of Users", min_value=1, value=100)
spawn_rate = st.number_input("⚡ Spawn Rate", min_value=1, value=100)
run_time = "10s"

if st.button("🚀 Run Now"):
    if not receiver_email:
        st.warning("Please enter a receiver email.")
    else:
        run_locust_and_send_report(receiver_email, users, spawn_rate, run_time)

scheduled_time = st.text_input("⏰ Schedule Daily Run Time (HH:MM 24hr)", value="14:21")

if st.button("📅 Schedule Daily Run"):
    try:
        datetime.strptime(scheduled_time, "%H:%M")
        schedule_daily_run(receiver_email, users, spawn_rate, run_time, scheduled_time)
    except ValueError:
        st.error("❌ Invalid time format. Use HH:MM in 24hr format.")

if st.button("📄 Show Latest Report"):
    if os.path.exists("locust_reports"):
        reports = sorted(os.listdir("locust_reports"), reverse=True)
        if reports:
            latest = os.path.join("locust_reports", reports[0])
            with open(latest, 'r', encoding='utf-8') as f:
                html = f.read()
            st.components.v1.html(html, height=600, scrolling=True)
        else:
            st.warning("No reports found.")
    else:
        st.warning("No reports directory exists yet.")
