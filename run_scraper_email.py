import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from linkedin_scraper import get_jobs

# Load credentials
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASS = os.environ["GMAIL_PASS"]

# Scrape jobs
jobs = get_jobs()
print(f"Found {len(jobs)} valid jobs")

if not jobs:
    print("❌ No jobs to send.")
    exit()

# Create HTML body
body = "<h2>🧑‍💻 <span style='color:#50006b;'>New LinkedIn Software Engineer Jobs (Last 24h)</span></h2><ul>"
for job in jobs:
    title = job.get("title", "").strip()
    company = job.get("company", "").strip()
    location = job.get("location", "N/A").strip()
    url = job.get("url", "#").strip()

    body += f"<li><strong>{title} at {company}</strong><br>📍 {location}<br><a href='{url}'>Apply</a></li><br>"
body += "</ul>"

# Compose email
msg = MIMEMultipart("alternative")
msg["Subject"] = "🧑‍💻 LinkedIn Job Updates (Last 24h)"
msg["From"] = GMAIL_USER
msg["To"] = GMAIL_USER
msg.attach(MIMEText(body, "html"))

# Send email using smtplib (TLS on port 587)
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        print("✅ Email sent successfully.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")