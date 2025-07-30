from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_jobs():
    options = Options()
    options.add_argument('--headless=new')  # Enable for background automation
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=United%20States&f_TPR=r86400")
    time.sleep(5)  # initial load

    # Step 1: Scroll the left-side job list container to load more jobs
    try:
        scroll_container = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
        for _ in range(10):  # Scroll more times to load more jobs
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
            time.sleep(1)
    except Exception as e:
        print(f"⚠️ Scroll container not found or failed: {e}")

    time.sleep(2)  # final buffer

    jobs = []
    job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
    print(f"🧪 Found {len(job_cards)} job cards.")

    for card in job_cards:
        try:
            # Ensure LinkedIn lazy-loads this card content
            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(0.4)

            title = card.find_element(By.CSS_SELECTOR, ".base-search-card__title").text.strip()
            company = card.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle").text.strip()
            location = card.find_element(By.CSS_SELECTOR, ".job-search-card__location").text.strip()
            url = card.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]

            print(f"📌 {title} at {company} — {location}")

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "url": url
            })

        except Exception as e:
            print(f"⚠️ Skipping card due to: {e}")
            continue

    driver.quit()
    return jobs