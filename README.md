
**🚀 AI-Driven Regression & Load Testing Automation Platform using GenAI (Groq LLaMA 3.1)**

 **📌 Introduction**
 
This project delivers a **robust AI-powered testing automation platform** that combines **Regression Testing** and **Load Testing** into a unified solution.  
It leverages **Groq’s LLaMA 3.1 API** for AI-driven script generation, **Selenium + PyTest** for regression testing, and **Locust** for load testing — all controlled via a **Streamlit dashboard** with **Jenkins CI/CD** integration.
---
**👨‍💻 Team – Hacktastic Squad**

Renuka S – Project Lead & GenAI Integration

Priyadharshini J – Load Testing & Performance

Rajavel P – Regression Automation

Sangavi K – Frontend & Dashboard

Lathika P – Reporting & Documentation

---
**✅ Regression Testing**

- AI-generated PyTest test cases from web forms
- Page Object Model (POM) for scalability
- Multi-browser support (Chrome, Firefox, Edge)
- Automatic screenshots for failed tests
- Rich Allure HTML reports with visual debugging
- Google Drive & Email integration for report sharing


**✅ Load Testing**

- AI-generated Locust scripts for APIs (DummyJSON, FakeStoreAPI, FakeApiNet)
- CRUD operation detection for APIs
- Parallel execution across multiple hosts
- Real-time logs & failure detection
- HTML performance reports with email delivery



**✅ CI/CD & Automation**

- Jenkins scheduled builds and test execution
- Allure & HTML Publisher plugins for hosted reports
- Email Extension plugin for automated notifications
- Secure credential handling using `.gitignore`


🚀 How to Run

🔹 Regression Testing
cd Regression_testing
streamlit run app1.py

🔹 Load Testing
cd Load_Testing
streamlit run main.py

📈 Reporting
Allure Reports → Pass/Fail status, screenshots, execution time, metadata
HTML Reports → Performance metrics for load tests

=======
**📂 Folder Structure (Visual Tree)**
```plaintext
Automation_Testing/
├── Regression_testing/
│   ├── Output/                  # Pytest results & reports
│   ├── Pages/                   # Page Object Model files
│   │   ├── base_page.py
│   │   ├── checkout_page.py
│   │   ├── footer_page.py
│   │   ├── login_page.py
│   │   ├── product_page.py
│   ├── pytest_report/            # Allure/HTML reports
│   ├── Screenshots/              # Failure screenshots
│   ├── test1/ test2/ test3/ test4/
│   │   ├── allure-report/
│   │   ├── allure-results/
│   │   ├── pytest_report/
│   │   ├── screenshots/
│   │   ├── client_secret.json
│   │   ├── secrets.json
│   │   ├── token.pkl
│   │   ├── main.py
│   │   ├── test_computing_and_interaactivity.py
│   │   ├── test_parameterize_demowebshop.py
│   │   ├── test_parameerize_maincategories.py
│   ├── utils/
│   │   ├── form_extractor1.py
│   │   ├── test_case_generator1.py
│   ├── app1.py                   # Streamlit dashboard UI
│   ├── confest1.py
│   ├── main.py
│   ├── config.json
│
├── Load_Testing/
│   ├── locust_reports/           # Load test HTML reports
│   ├── locust_scripts/           # AI-generated Locust scripts
│   ├── logs/                     # Execution logs
│   │   ├── failed_hosts.txt
│   ├── ai_generator.py
│   ├── generate_locust_code.py
│   ├── locust_scheduler.py
│   ├── locustfile.py
│   ├── main.py
│   ├── run_test.py
│   ├── config.json
│   ├── secrets.json
│   ├── locust_output.log

🚀 How to Run

🔹 Regression Testing
cd Regression_testing
streamlit run app1.py

🔹 Load Testing
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
Jira ticket auto-generation
AI-powered self-healing test scripts
Grafana/Prometheus dashboards for monitoring

=======

📜 Detailed Project Description
Regression Testing
The Selenium Test Automation & Reporting System is an end-to-end automation framework designed to simplify and accelerate the process of generating, executing, and reporting Selenium + Pytest-based test cases.
It integrates browser-based form exploration, AI-powered test case generation, dynamic test execution, and automated Allure reporting — all accessible through a Streamlit dashboard, enabling QA teams to automate regression workflows with minimal manual effort.

Key components include:
Form Extractor: Navigates user-defined flows and collects web elements using Selenium WebDriver.
AI Test Generator: Leverages Groq’s LLaMA 3.1 model to create Pytest test functions based on extracted content and scenarios.
Executor & Screenshot Handler: Captures screenshots for failed test cases, automatically embedding them in Allure reports.

Automation Features:
Allure report generator produces rich, interactive HTML reports.
Daily automated test execution and result sharing via Email and Google Drive API.
Jenkins integration with Allure Report, HTML Publisher, and Email Extension plugins.
Follows Page Object Model (POM) for maintainability.
Supports parallel execution with pytest-xdist.
Multi-browser support: Chrome, Edge, Firefox.
Built using Python, Selenium, Pytest, Allure, Streamlit, Groq LLM, and Google Drive API.

Load Testing
The Load Testing Automation System enables intelligent and streamlined performance testing of web applications.
Instead of relying on manually written test scripts, it uses Groq’s LLaMA3 API to automatically generate Locust test scripts tailored to the target website.

Key capabilities:
Supports multiple hosts: DummyJSON, FakeStoreAPI, FakeApiNet.
Automatically detects CRUD operations (Create, Read, Update, Delete).
Parallel execution across multiple APIs for performance comparison.
Configurable test parameters via Streamlit UI (users, spawn rate, duration).
Real-time logs, countdown timers, and failure capture.
Automatic HTML report generation and email delivery.
Supports daily scheduling and automated reporting.

Overall Definition
Our platform delivers a robust AI-driven Regression and Load Testing Automation framework designed for:
Minimal manual effort
Maximum automation
AI-based script generation (Groq’s LLaMA 3.1)
Unified regression & load testing control via Streamlit UI
CI/CD automation with Jenkins
Smart reporting and sharing via Google Drive and Email

Workflow Summary:
User configures tests via Streamlit UI.
AI generates Selenium/PyTest or Locust scripts.
Tests execute (parallel supported).
Reports generated → uploaded → emailed.
Jenkins handles scheduling, automation, and publishing.


