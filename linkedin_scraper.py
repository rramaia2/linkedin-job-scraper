from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_jobs():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=United%20States&f_TPR=r86400")

    time.sleep(5)
    jobs = []

    listings = driver.find_elements(By.CSS_SELECTOR, ".base-card")

    for listing in listings:
        try:
            title = listing.find_element(By.CSS_SELECTOR, ".base-search-card__title").text.strip()
            company = listing.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle").text.strip()
            location = listing.find_element(By.CSS_SELECTOR, ".job-search-card__location").text.strip()
            link = listing.find_element(By.CSS_SELECTOR, "a").get_attribute("href").split("?")[0]

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "url": link
            })
        except:
            continue

    driver.quit()
    return jobs