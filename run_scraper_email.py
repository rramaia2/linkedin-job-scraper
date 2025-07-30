import os
import yagmail
from linkedin_scraper import get_jobs

# Email credentials from env
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASS = os.environ["GMAIL_PASS"]

jobs = get_jobs()

print(f"Found {len(jobs)} total jobs")

if jobs:
    body = "<h2>🧑‍💻 <span style='color:#50006b;'>New LinkedIn Software Engineer Jobs (Last 24h)</span></h2><ul>"

    for job in jobs:
        title = job.get("title", "No Title")
        company = job.get("company", "Unknown Company")
        location = job.get("location", "N/A")
        url = job.get("url", "#")

        body += f"<li><strong>{title} at {company}</strong><br>📍 {location}<br><a href='{url}'>Apply</a></li><br>"

    body += "</ul>"

    yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)
    yag.send(to=GMAIL_USER, subject="🧑‍💻 LinkedIn Job Updates (= 24h)", contents=body)
else:
    print("❌ No jobs found.")