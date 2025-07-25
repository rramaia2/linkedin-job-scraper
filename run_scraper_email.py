import json
import os
import yagmail
from linkedin_scraper import get_jobs

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASS = os.environ["GMAIL_PASS"]

# Load previous sent jobs
if os.path.exists("sent_jobs.json"):
    with open("sent_jobs.json", "r") as f:
        sent_urls = set(json.load(f))
else:
    sent_urls = set()

jobs = get_jobs()
new_jobs = [job for job in jobs if job["url"] not in sent_urls]

if new_jobs:
    # Prepare HTML
    body = "<h3>🧑‍💻 New LinkedIn Software Engineer Jobs</h3><ul>"
    for job in new_jobs:
        body += f"<li><b>{job['title']}</b> at {job['company']} - {job['location']}<br><a href='{job['url']}'>Apply</a></li>"
    body += "</ul>"

    # Send Email
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)
    yag.send(to=GMAIL_USER, subject="🧑‍💻 LinkedIn Job Updates", contents=body)

    # Save sent URLs
    sent_urls.update(job["url"] for job in new_jobs)
    with open("sent_jobs.json", "w") as f:
        json.dump(list(sent_urls), f)
else:
    print("No new jobs to send.")