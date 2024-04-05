import smtplib
from email.mime.text import MIMEText

smtp_server = "smtp.mailgun.org"
smtp_port = 587
smtp_username = "postmaster@sandbox342c892e32d3490bbe29d996ee36ad19.mailgun.org"
smtp_password = "3430802f6c0158f57624cfb53ae23773-309b0ef4-21aed5ff"
from_addr = smtp_username
to_addr = "kevingopito@gmail.com"  # Replace with an authorized recipient

msg = MIMEText("This is a test email from Mailgun.")
msg["Subject"] = "Test Email"
msg["From"] = from_addr
msg["To"] = to_addr

s = smtplib.SMTP(smtp_server, smtp_port)
s.starttls()
s.login(smtp_username, smtp_password)
s.sendmail(from_addr, [to_addr], msg.as_string())
s.quit()

