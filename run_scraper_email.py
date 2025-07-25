import json
import os
import yagmail
from linkedin_scraper import get_jobs

# Load Gmail credentials from environment
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASS = os.environ["GMAIL_PASS"]

# Load previously sent job URLs (deduplication)
if os.path.exists("sent_jobs.json"):
    with open("sent_jobs.json", "r") as f:
        sent_urls = set(json.load(f))
else:
    sent_urls = set()

# Scrape new job postings
jobs = get_jobs()
new_jobs = [job for job in jobs if job.get("url") and job["url"] not in sent_urls]

print(f"Found {len(jobs)} jobs, {len(new_jobs)} new jobs")

if new_jobs:
    # Start email body
    body = "<h2>🧑‍💻 <span style='color:#50006b;'>New LinkedIn Software Engineer Jobs</span></h2><ul>"

    for job in new_jobs:
        title = job.get("title", "").strip()
        company = job.get("company", "").strip()
        location = job.get("location", "").strip()
        url = job.get("url", "").strip()

        if not title and not company:
            continue  # Skip completely blank entries

        body += f"<li><strong>{title or 'No Title'} at {company or 'Unknown Company'}</strong><br>📍 {location or 'N/A'}<br><a href='{url}'>Apply</a></li><br>"

    body += "</ul>"

    # Send the email
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)
    yag.send(to=GMAIL_USER, subject="🧑‍💻 LinkedIn Job Updates", contents=body)

    # Update sent job URLs
    sent_urls.update(job["url"] for job in new_jobs)
    with open("sent_jobs.json", "w") as f:
        json.dump(list(sent_urls), f)

else:
    print("✅ No new jobs to send today.")