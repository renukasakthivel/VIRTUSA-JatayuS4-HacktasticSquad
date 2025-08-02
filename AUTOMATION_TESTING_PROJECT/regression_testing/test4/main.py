import streamlit as st
import os
import subprocess
import zipfile
import smtplib
from email.message import EmailMessage
from datetime import datetime
import threading
import schedule
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import shutil
import json

with open("secrets.json") as f:
    secrets = json.load(f)

TEST_DIR = r"D:\AUTOMATION_TESTING\AUTOMATION_TESTING_PROJECT\regression_testing\test4"
ALLURE_RESULTS_DIR = os.path.join(TEST_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(TEST_DIR, "allure-report")
ALLURE_PATH = secrets["allure_path"]
SENDER_EMAIL = secrets["email"]
SENDER_PASSWORD = secrets["password"]
CREDENTIALS_FILE = secrets["credentials_file"]
TOKEN_PICKLE = "token.pkl"
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# === Global Lock ===
is_running = False

# === Streamlit Setup ===
st.set_page_config(page_title="Regression Test Runner", layout="centered")
st.title("🧪 Regression Testing Automation Dashboard")

receiver_email = st.text_input("📥 Enter Receiver Email")
scheduled_time = st.text_input("⏰ Set Daily Schedule Time (HH:MM)", value="14:10")

# === Core Functions ===

def run_pytest():
    try:
        if os.path.exists(ALLURE_RESULTS_DIR):
            shutil.rmtree(ALLURE_RESULTS_DIR)
        os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

        result = subprocess.run(
            ["pytest", TEST_DIR, "--alluredir", ALLURE_RESULTS_DIR],
            check=True, capture_output=True, text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Test execution failed.")
        print(e.stdout + "\n" + e.stderr)

def generate_allure_report():
    try:
        if os.path.exists(ALLURE_REPORT_DIR):
            shutil.rmtree(ALLURE_REPORT_DIR)

        subprocess.run(
            [ALLURE_PATH, "generate", ALLURE_RESULTS_DIR, "--clean", "-o", ALLURE_REPORT_DIR],
            shell=True, check=True
        )
        print("✅ Allure report generated.")
    except Exception as e:
        print(f"❌ Failed to generate report: {e}")

def parse_allure_results():
    results = []
    for file in os.listdir(ALLURE_RESULTS_DIR):
        if file.endswith("result.json"):
            with open(os.path.join(ALLURE_RESULTS_DIR, file), "r") as f:
                try:
                    data = json.load(f)
                    results.append(data)
                except Exception as e:
                    print(f"⚠ Could not parse {file}: {e}")
    return results

def zip_allure_report():
    try:
        if not os.path.exists(ALLURE_REPORT_DIR) or not os.listdir(ALLURE_REPORT_DIR):
            raise Exception("Allure report directory is missing or empty.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"allure-report-{timestamp}.zip"
        zip_path = os.path.join(TEST_DIR, zip_filename)

        for file in os.listdir(TEST_DIR):
            if file.startswith("allure-report-") and file.endswith(".zip"):
                try:
                    os.remove(os.path.join(TEST_DIR, file))
                except Exception as e:
                    print(f"⚠ Could not remove old file: {file} — {e}")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(ALLURE_REPORT_DIR):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, start=ALLURE_REPORT_DIR)
                    zipf.write(filepath, arcname)
        print(f"✅ Report zipped: {zip_path}")
        return zip_path
    except Exception as e:
        print(f"❌ Zipping failed: {e}")
        return None

def authenticate_drive():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path):
    try:
        service = authenticate_drive()
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype='application/zip')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        service.permissions().create(fileId=file['id'], body={'role': 'reader', 'type': 'anyone'}).execute()
        return f"https://drive.google.com/uc?id={file['id']}&export=download"
    except Exception as e:
        print(f"❌ Drive upload failed: {e}")
        return None

def send_email_with_link(download_link, to_email):
    try:
        msg = EmailMessage()
        msg["Subject"] = "🧪 Allure Report Download Link"
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg.set_content(f"The latest Allure report is ready.\n\nDownload link:\n{download_link}\n\nRegards,\nAutomation System")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent to:", to_email)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# === Full Workflow ===

def full_test_workflow(receiver_email):
    global is_running
    if is_running:
        print("⚠ Another job is already running. Skipping this cycle.")
        return
    is_running = True
    print(f"\n🚀 Starting workflow for {receiver_email}")

    try:
        run_pytest()
        generate_allure_report()
        parse_allure_results()
        zip_path = zip_allure_report()
        if zip_path:
            link = upload_to_drive(zip_path)
            if link:
                send_email_with_link(link, receiver_email)
            else:
                print("⚠ Skipping email — upload failed.")
        else:
            print("⚠ Skipping upload and email — no ZIP created.")
    finally:
        is_running = False

# === Scheduler ===

def schedule_runner():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_schedule_job(receiver_email, time_str):
    schedule.clear()
    schedule.every().day.at(time_str).do(full_test_workflow, receiver_email=receiver_email)
    threading.Thread(target=schedule_runner, daemon=True).start()
    print(f"⏰ Scheduled job set for {time_str} every day.")

# === Streamlit UI Buttons ===

if st.button("▶ Run Tests & Share Report"):
    if receiver_email:
        full_test_workflow(receiver_email)
        st.success("✅ Tests completed, report sent.")
    else:
        st.warning("⚠ Please enter a recipient email.")

if st.button("📅 Schedule Daily Run"):
    try:
        datetime.strptime(scheduled_time, "%H:%M")
        if receiver_email:
            start_schedule_job(receiver_email, scheduled_time)
            st.success(f"📆 Daily run scheduled at {scheduled_time} for {receiver_email}")
        else:
            st.warning("⚠ Please enter a recipient email to schedule.")
    except ValueError:
        st.error("❌ Invalid time format! Use HH:MM (24hr format).")

# === Download Button for Latest ZIP ===

latest_zip = None
for file in sorted(os.listdir(TEST_DIR), reverse=True):
    if file.startswith("allure-report-") and file.endswith(".zip"):
        latest_zip = os.path.join(TEST_DIR, file)
        break

if latest_zip:
    with open(latest_zip, "rb") as zip_file:
        st.download_button(
            label="📥 Download Latest Allure Report ZIP",
            data=zip_file,
            file_name=os.path.basename(latest_zip),
            mime="application/zip"
        )





# import streamlit as st
# import os
# import subprocess
# import zipfile
# import smtplib
# from email.message import EmailMessage
# from datetime import datetime
# import threading
# import schedule
# import time
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# import pickle
# import shutil

# # === Constants ===
# TEST_DIR = r"D:\AUTOMATION_TESTING\AUTOMATION_TESTING_PROJECT\regression_testing\test4"
# ALLURE_RESULTS_DIR = os.path.join(TEST_DIR, "allure-results")
# ALLURE_REPORT_DIR = os.path.join(TEST_DIR, "allure-report")
# ALLURE_PATH = r"C:\Users\Admin\Downloads\allure-2.34.1\bin\allure.bat"
# SENDER_EMAIL = "rajavelit22@gmail.com"
# SENDER_PASSWORD = "kslh raub kfag ogyj"
# CREDENTIALS_FILE = "client_secret_388471591533-1du8fqlgtd3c0m5hj5hcosrpkt048h2p.apps.googleusercontent.com.json"
# TOKEN_PICKLE = "token.pkl"
# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# # === Global Lock ===
# is_running = False

# # === Streamlit Setup ===
# st.set_page_config(page_title="Regression Test Runner", layout="centered")
# st.title("🧪 Regression Testing Automation Dashboard")

# receiver_email = st.text_input("📥 Enter Receiver Email")
# scheduled_time = st.text_input("⏰ Set Daily Schedule Time (HH:MM)", value="14:10")

# # === Core Functions ===

# def run_pytest():
#     try:
#         if os.path.exists(ALLURE_RESULTS_DIR):
#             shutil.rmtree(ALLURE_RESULTS_DIR)
#         os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

#         result = subprocess.run(
#             ["pytest", TEST_DIR, "--alluredir", ALLURE_RESULTS_DIR],
#             check=True, capture_output=True, text=True
#         )
#         print(result.stdout)
#     except subprocess.CalledProcessError as e:
#         print("❌ Test execution failed.")
#         print(e.stdout + "\n" + e.stderr)

# def generate_allure_report():
#     try:
#         if os.path.exists(ALLURE_REPORT_DIR):
#             shutil.rmtree(ALLURE_REPORT_DIR)

#         subprocess.run(
#             [ALLURE_PATH, "generate", ALLURE_RESULTS_DIR, "--clean", "-o", ALLURE_REPORT_DIR],
#             shell=True, check=True
#         )
#         print("✅ Allure report generated.")
#     except Exception as e:
#         print(f"❌ Failed to generate report: {e}")

# def zip_allure_report():
#     try:
#         if not os.path.exists(ALLURE_REPORT_DIR) or not os.listdir(ALLURE_REPORT_DIR):
#             raise Exception("Allure report directory is missing or empty.")

#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         zip_filename = f"allure-report-{timestamp}.zip"
#         zip_path = os.path.join(TEST_DIR, zip_filename)

#         # Clean old zips
#         for file in os.listdir(TEST_DIR):
#             if file.startswith("allure-report-") and file.endswith(".zip"):
#                 try:
#                     os.remove(os.path.join(TEST_DIR, file))
#                 except Exception as e:
#                     print(f"⚠ Could not remove old file: {file} — {e}")

#         with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
#             for root, _, files in os.walk(ALLURE_REPORT_DIR):
#                 for file in files:
#                     filepath = os.path.join(root, file)
#                     arcname = os.path.relpath(filepath, start=ALLURE_REPORT_DIR)
#                     zipf.write(filepath, arcname)
#         print(f"✅ Report zipped: {zip_path}")
#         return zip_path
#     except Exception as e:
#         print(f"❌ Zipping failed: {e}")
#         return None

# def authenticate_drive():
#     creds = None
#     if os.path.exists(TOKEN_PICKLE):
#         with open(TOKEN_PICKLE, 'rb') as token:
#             creds = pickle.load(token)
#     if not creds:
#         flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open(TOKEN_PICKLE, 'wb') as token:
#             pickle.dump(creds, token)
#     return build('drive', 'v3', credentials=creds)

# def upload_to_drive(file_path):
#     try:
#         service = authenticate_drive()
#         file_metadata = {'name': os.path.basename(file_path)}
#         media = MediaFileUpload(file_path, mimetype='application/zip')
#         file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#         service.permissions().create(fileId=file['id'], body={'role': 'reader', 'type': 'anyone'}).execute()
#         return f"https://drive.google.com/uc?id={file['id']}&export=download"
#     except Exception as e:
#         print(f"❌ Drive upload failed: {e}")
#         return None

# def send_email_with_link(download_link, to_email):
#     try:
#         msg = EmailMessage()
#         msg["Subject"] = "🧪 Allure Report Download Link"
#         msg["From"] = SENDER_EMAIL
#         msg["To"] = to_email
#         msg.set_content(f"The latest Allure report is ready.\n\nDownload link:\n{download_link}\n\nRegards,\nAutomation System")

#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#             smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
#             smtp.send_message(msg)
#         print("✅ Email sent to:", to_email)
#     except Exception as e:
#         print(f"❌ Failed to send email: {e}")

# # === Full Workflow ===

# def full_test_workflow(receiver_email):
#     global is_running
#     if is_running:
#         print("⚠ Another job is already running. Skipping this cycle.")
#         return
#     is_running = True
#     print(f"\n🚀 Starting workflow for {receiver_email}")

#     try:
#         run_pytest()
#         generate_allure_report()
#         zip_path = zip_allure_report()
#         if zip_path:
#             link = upload_to_drive(zip_path)
#             if link:
#                 send_email_with_link(link, receiver_email)
#             else:
#                 print("⚠ Skipping email — upload failed.")
#         else:
#             print("⚠ Skipping upload and email — no ZIP created.")
#     finally:
#         is_running = False

# # === Scheduler ===

# def schedule_runner():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def start_schedule_job(receiver_email, time_str):
#     schedule.clear()
#     schedule.every().day.at(time_str).do(full_test_workflow, receiver_email=receiver_email)
#     threading.Thread(target=schedule_runner, daemon=True).start()
#     print(f"⏰ Scheduled job set for {time_str} every day.")

# # === Streamlit UI Buttons ===

# if st.button("▶ Run Tests & Share Report"):
#     if receiver_email:
#         full_test_workflow(receiver_email)
#         st.success("✅ Tests completed, report sent.")
#     else:
#         st.warning("⚠ Please enter a recipient email.")

# if st.button("📅 Schedule Daily Run"):
#     try:
#         datetime.strptime(scheduled_time, "%H:%M")
#         if receiver_email:
#             start_schedule_job(receiver_email, scheduled_time)
#             st.success(f"📆 Daily run scheduled at {scheduled_time} for {receiver_email}")
#         else:
#             st.warning("⚠ Please enter a recipient email to schedule.")
#     except ValueError:
#         st.error("❌ Invalid time format! Use HH:MM (24hr format).")

# # === Download Button for Latest ZIP ===

# latest_zip = None
# for file in sorted(os.listdir(TEST_DIR), reverse=True):
#     if file.startswith("allure-report-") and file.endswith(".zip"):
#         latest_zip = os.path.join(TEST_DIR, file)
#         break

# if latest_zip:
#     with open(latest_zip, "rb") as zip_file:
#         st.download_button(
#             label="📥 Download Latest Allure Report ZIP",
#             data=zip_file,
#             file_name=os.path.basename(latest_zip),
#             mime="application/zip"
#         )