from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google import genai

def get_form_text(form_url):
    try:
        # Path to your local ChromeDriver
        driver_path = "C:/Users/Aravind Jayakumar/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
        service = Service(driver_path)
        options = Options()
        options.add_argument("--headless")  # Run in headless mode (no visible window)
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=service, options=options)

        # Load the Google Form
        driver.get(form_url)

        # Wait for the form to load and extract elements
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".o3Dpx")))
        elements_text = [element.text for element in elements]

        driver.quit()
        return elements_text

    except Exception as e:
        return f"Error loading form: {e}"

def get_gemini_response(input_text):
    genai_client = genai.Client(api_key="AIzaSyAfO8S5sipCLNhMgt70HtpFDrpuI7nanfw")
    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input_text
    )
    return response.text

def analyze_form_with_gemini(form_url):
    form_content = get_form_text(form_url)
    
    if isinstance(form_content, str):  # If it's an error message
        return form_content
    else:
        return get_gemini_response(form_content)
