import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 1. Load recruiter list
df = pd.read_csv('recruiters.csv')

# 2. Load email template
with open("email_template.txt", "r") as f:
    template = f.read()

YOUR_EMAIL = "rajdeepgolan@gmail.com"
YOUR_APP_PASSWORD = "dlbs*lcog*gmis*vcfz"
RESUME_PATH = "Rajdeep_Golan_Resume.pdf"  # your attachment

# 3. Setup SMTP
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(YOUR_EMAIL, YOUR_APP_PASSWORD)

for index, row in df.iterrows():
    name = row["name"]
    email = row["email"]

    # personalize message
    personalized_msg = template.format(name=name)

    msg = MIMEMultipart()
    msg["From"] = YOUR_EMAIL
    msg["To"] = email
    msg["Subject"] = "Software Engineer (5 YOE | Masters AI) - Why I'm a fit for Meta"

    # add the email text
    msg.attach(MIMEText(personalized_msg, "plain"))

    # add resume attachment
    with open(RESUME_PATH, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {RESUME_PATH}",
    )
    msg.attach(part)

    # send email
    server.sendmail(YOUR_EMAIL, email, msg.as_string())
    print(f"Email sent to {name} ({email})")

server.quit()
print("All emails sent successfully!")