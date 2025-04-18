from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai  # fixed incorrect import

def get_form_text(form_url):
    try:
        # Linux paths
        chrome_binary_path = "/usr/bin/chromium"
        chromedriver_path = "/app/chromedriver"

        # Set Chrome options
        options = Options()
        options.binary_location = chrome_binary_path
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)

        # Open the Google Form
        driver.get(form_url)

        # Wait and extract form elements
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".o3Dpx")))
        elements_text = [element.text for element in elements]

        driver.quit()
        return elements_text

    except Exception as e:
        return f"Error loading form: {e}"

def get_gemini_response(input_text):
    genai_client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input_text
    )
    return response.text

def analyze_form_with_gemini(form_url):
    form_content = get_form_text(form_url)

    if isinstance(form_content, str):  # error string
        return form_content
    else:
        return get_gemini_response(form_content)
