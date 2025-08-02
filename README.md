# 🚀 AI-Driven Regression & Load Testing Automation Platform using GenAI (Groq LLaMA 3.1)

## 📌 Introduction
This project delivers a **robust AI-powered testing automation platform** that combines **Regression Testing** and **Load Testing** into a unified solution.  
It leverages **Groq’s LLaMA 3.1 API** for AI-driven script generation, **Selenium + PyTest** for regression testing, and **Locust** for load testing — all controlled via a **Streamlit dashboard** with **Jenkins CI/CD** integration.

---

## 🛠 Features

### ✅ Regression Testing
- AI-generated PyTest test cases from web forms
- Page Object Model (POM) for scalability
- Multi-browser support (Chrome, Firefox, Edge)
- Automatic screenshots for failed tests
- Rich Allure HTML reports with visual debugging
- Google Drive & Email integration for report sharing

### ✅ Load Testing
- AI-generated Locust scripts for APIs (DummyJSON, FakeStoreAPI, FakeApiNet)
- CRUD operation detection for APIs
- Parallel execution across multiple hosts
- Real-time logs & failure detection
- HTML performance reports with email delivery

### ✅ CI/CD & Automation
- Jenkins scheduled builds and test execution
- Allure & HTML Publisher plugins for hosted reports
- Email Extension plugin for automated notifications
- Secure credential handling using `.gitignore`

---

## 📂 Folder Structure
Automation_Testing/
├── Regression_testing/
│ ├── Output/
│ ├── Pages/
│ ├── pytest_report/
│ ├── Screenshots/
│ ├── test1/ test2/ test3/ test4/
│ ├── utils/
│ ├── app1.py
│ ├── main.py
│ ├── config.json
├── Load_Testing/
│ ├── locust_reports/
│ ├── locust_scripts/
│ ├── logs/
│ ├── ai_generator.py
│ ├── generate_locust_code.py
│ ├── locust_scheduler.py
│ ├── locustfile.py
│ ├── main.py
│ ├── run_test.py
│ ├── config.json
│ ├── secrets.json

yaml
Copy
Edit

---

## 🚀 How to Run

### 🔹 Regression Testing
```bash
cd Regression_testing
streamlit run app1.py
🔹 Load Testing
bash
Copy
Edit
cd Load_Testing
streamlit run main.py
📈 Reporting
Allure Reports → Pass/Fail status, screenshots, execution time, metadata

HTML Reports → Performance metrics for load tests

Reports auto-uploaded to Google Drive & emailed to stakeholders

🔮 Future Enhancements
Slack alert integration

Jira ticket auto-generation

AI-powered self-healing test scripts

Grafana/Prometheus dashboards for monitoring

👨‍💻 Team – Hacktastic Squad
Renuka S – Project Lead & GenAI Integration

Priyadharshini J – Load Testing & Performance

Rajavel P – Regression Automation

Sangavi K – Frontend & Dashboard

Lathika P – Reporting & Documentation