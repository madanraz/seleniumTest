import os
import time
import pickle
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIG ---
CHROME_DRIVER_PATH = "chromedriver"
CACHE_DIR = "internship_cache"

os.makedirs(CACHE_DIR, exist_ok=True)

# --- UTILITY FUNCTIONS ---

def get_cache_path(url):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.pkl")

def load_from_cache(url):
    path = get_cache_path(url)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_to_cache(url, data):
    path = get_cache_path(url)
    with open(path, "wb") as f:
        pickle.dump(data, f)

# --- MAIN SCRAPER FUNCTION FOR CUVETTE ---

def fetch_cuvette_internships(url):
    service = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless=chrome")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'StudentInternshipCard_container__iBvIw'))
    )

    internships = driver.find_elements(By.CLASS_NAME, 'StudentInternshipCard_container__iBvIw')
    job_data_list = []

    for card in internships:
        job_data = {}

        try:
            job_data['title'] = card.find_element(By.CSS_SELECTOR, 'h3').text
        except:
            job_data['title'] = ''

        try:
            desc = card.find_element(By.CSS_SELECTOR, '.StudentInternshipCard_heading__7IIA7 p').text
            if '|' in desc:
                company, location = desc.split('|')
                job_data['company'] = company.strip()
                job_data['location'] = location.strip()
            else:
                job_data['company'] = desc.strip()
                job_data['location'] = ''
        except:
            job_data['company'] = ''
            job_data['location'] = ''

        try:
            skills = card.find_elements(By.CLASS_NAME, 'StudentInternshipCard_skill__SLTVX')
            job_data['skills'] = [skill.text for skill in skills]
        except:
            job_data['skills'] = []

        try:
            job_data['stipend'] = card.find_element(By.XPATH, ".//*[text()='Stipend per month']/following-sibling::div").text
        except:
            job_data['stipend'] = ''

        try:
            job_data['duration'] = card.find_element(By.XPATH, ".//*[text()='Duration']/following-sibling::div").text
        except:
            job_data['duration'] = ''

        try:
            job_data['mode'] = card.find_element(By.XPATH, ".//*[text()='Mode']/following-sibling::div").text
        except:
            job_data['mode'] = ''

        try:
            job_data['start_date'] = card.find_element(By.XPATH, ".//*[text()='Start Date']/following-sibling::div").text
        except:
            job_data['start_date'] = ''

        try:
            job_data['openings'] = card.find_element(By.XPATH, ".//p[contains(text(), '#Openings')]/following-sibling::div").text
        except:
            job_data['openings'] = ''

        try:
            footer = card.find_element(By.CLASS_NAME, 'StudentInternshipCard_currentInfoLeft__NkjBF').text
            job_data['deadline_posted'] = footer
        except:
            job_data['deadline_posted'] = ''

        try:
            job_data['details_link'] = card.find_element(By.LINK_TEXT, "View Details").get_attribute("href")
        except:
            job_data['details_link'] = ''

        job_data_list.append(job_data)

    driver.quit()
    return job_data_list

# --- MAIN WRAPPER FUNCTION ---

def get_cuvette_internships(url, refresh=False):
    if not refresh:
        cached_data = load_from_cache(url)
        if cached_data:
            print("Loaded from cache.")
            return cached_data

    print("Fetching fresh data from the web...")
    data = fetch_cuvette_internships(url)
    save_to_cache(url, data)
    return data

# --- USAGE EXAMPLE ---

if __name__ == "__main__":
    url = "https://cuvette.tech/jobs/internships"
    data = get_cuvette_internships(url, refresh=False)  # Set refresh=True to force reload

    for idx, internship in enumerate(data, 1):
        print(f"Internship {idx}:")
        for key, value in internship.items():
            print(f"{key}: {value}")
        print('-' * 50)
