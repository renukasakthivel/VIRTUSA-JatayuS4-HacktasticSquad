import streamlit as st
import json
import os
from utils.form_extractor1 import extract_all_elements
from utils.test_case_generator1 import generate_prompt, generate_test_case

st.set_page_config(page_title="🧪 Selenium Test Generator")

# Load API key
config = json.load(open("config.json"))
os.environ["GROQ_API_KEY"] = config["GROQ_API_KEY"]

st.title("🔧 Selenium + Pytest Test Case Generator")

# --- Browser Selection ---
browser_choice = st.selectbox("Select Browser", ["Chrome", "Edge", "Firefox"])

chrome_driver_path = st.text_input(
    "Chrome Driver Path",
      value=r"E:\Stage3\Testing\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
)
edge_driver_path = st.text_input(
    "Edge Driver Path",
     value=r"C:\Users\Admin\Downloads\edgedriver_win64 (1)\msedgedriver.exe"
)
firefox_driver_path = st.text_input(
    "Firefox Driver Path",
    value=r"C:\Users\Admin\Downloads\geckodriver.exe"
)

# Determine driver path
if browser_choice == "Chrome":
    selected_driver_path = chrome_driver_path
elif browser_choice == "Edge":
    selected_driver_path = edge_driver_path
else:
    selected_driver_path = firefox_driver_path

# --- Test Configuration Inputs ---
url = st.text_input("Page URL", placeholder="https://example.com")
username = st.text_input("Username (if login required)", value="", key="username")
password = st.text_input("Password (if login required)", type="password", key="password")
test_flow = st.text_input("Test Flow (e.g., 'Login → Inventory → Cart → Checkout → Logout')")
test_type = st.text_input("Test Scenario Description (e.g., 'Complete purchase flow')")
conditions = st.text_area("Additional Test Conditions (Optional)")

if st.button("Generate Test Case"):
    if not url or not selected_driver_path or not test_flow:
        st.warning("⚠ Please fill in the required fields: URL, Driver Path, and Test Flow.")
    else:
        with st.spinner("🔍 Extracting page elements and generating test case..."):
            all_fields = []
            flow_pages = test_flow.split("→")

            for page in flow_pages:
                page = page.strip()
                page_url = f"{url}/{page.lower().replace(' ', '_')}"

                fields = extract_all_elements(
                    url=page_url,
                    driver_path=selected_driver_path,
                    browser=browser_choice.lower(),
                    username=username,
                    password=password
                )

                if not fields:
                    st.error(f"❌ No elements found on the '{page}' page.")
                    break
                else:
                    all_fields.append({"page": page, "fields": fields})

            if all_fields:
                prompt = generate_prompt(test_type, all_fields, url, conditions)
                code = generate_test_case(prompt, browser_choice, selected_driver_path)

                st.success("✅ Test case generated successfully!")
                st.code(code, language="python")

                os.makedirs("output", exist_ok=True)
                with open("output/selenium_test_case.py", "w", encoding="utf-8") as f:
                    f.write(code)

                with open("output/selenium_test_case.py", "rb") as f:
                    st.download_button("📥 Download Test Case", f, file_name="selenium_test_case.py")



# import streamlit as st
# import json
# import os
# from utils.form_extractor1 import extract_all_elements
# from utils.test_case_generator1 import generate_prompt, generate_test_case

# # Streamlit page config
# st.set_page_config(page_title="🧪 Selenium Test Generator")

# # Load API key from config.json
# config = json.load(open("config.json"))
# os.environ["GROQ_API_KEY"] = config["GROQ_API_KEY"]

# # Title
# st.title("🔧 Selenium + Pytest Test Case Generator")

# # --- Browser Selection and WebDriver Paths ---
# browser_choice = st.selectbox("Select Browser", ["Chrome", "Edge", "Firefox"])

# chrome_driver_path = st.text_input(
#     "Chrome Driver Path",
#      value=r"E:\Stage3\Testing\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
# )

# edge_driver_path = st.text_input(
#     "Edge Driver Path",
#      value=r"C:\Users\Admin\Downloads\edgedriver_win64 (1)\msedgedriver.exe"
# )

# firefox_driver_path = st.text_input(
#     "Firefox Driver Path",
#     value=r"C:\Users\Admin\Downloads\geckodriver.exe"
# )

# # Choose driver path based on selected browser
# if browser_choice == "Chrome":
#     selected_driver_path = chrome_driver_path
# elif browser_choice == "Edge":
#     selected_driver_path = edge_driver_path
# else:  # Firefox
#     selected_driver_path = firefox_driver_path

# # --- Test Configuration Inputs ---
# url = st.text_input("Page URL", placeholder="https://example.com")
# username = st.text_input("Username (if login required)", value="", key="username")
# password = st.text_input("Password (if login required)", type="password", key="password")
# test_flow = st.text_input("Test Flow (e.g., 'Login → Inventory → Cart → Checkout → Logout')")
# test_type = st.text_input("Test Scenario Description (e.g., 'Complete purchase flow')")
# conditions = st.text_area("Additional Test Conditions (Optional)")

# # --- Generate Test Case Button ---
# if st.button("Generate Test Case"):
#     if not url or not selected_driver_path or not test_flow:
#         st.warning("⚠ Please fill in the required fields: URL, Driver Path, and Test Flow.")
#     else:
#         with st.spinner("🔍 Extracting page elements and generating test case..."):
#             all_fields = []
#             flow_pages = test_flow.split("→")

#             for page in flow_pages:
#                 page = page.strip()
#                 page_url = f"{url}/{page.lower().replace(' ', '_')}"

#                 fields = extract_all_elements(
#                     url=page_url,
#                     driver_path=selected_driver_path,
#                     browser=browser_choice.lower(),
#                     username=username,
#                     password=password
#                 )

#                 if not fields:
#                     st.error(f"❌ No elements found on the '{page}' page.")
#                     break
#                 else:
#                     all_fields.append({"page": page, "fields": fields})

#             if all_fields:
#                 # ✅ Pass browser and driver path to generator
#                 prompt = generate_prompt(test_type, all_fields, url, conditions)
#                 code = generate_test_case(prompt, browser_choice, selected_driver_path)

#                 st.success("✅ Test case generated successfully!")
#                 st.code(code, language="python")

#                 os.makedirs("output", exist_ok=True)
#                 with open("output/selenium_test_case.py", "w", encoding="utf-8") as f:
#                     f.write(code)

#                 with open("output/selenium_test_case.py", "rb") as f:
#                     st.download_button("📥 Download Test Case", f, file_name="selenium_test_case.py")