import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
import json

class Email:
    def __init__(self):
        self.sender_addr = "tech_temco@outlook.com"
        self.sender_pass = "Techtemc0"
        self.sender_smtp_serv = "smtp.live.com"
        self.sender_smtp_serv_port = 587
        with open('config/user_infoUI.json', 'rb') as email_file:
            user_email_raw = json.load(email_file)
            email_file.close()
        self.recipients = user_email_raw['user_email']
        self.subject = "Git report"
        self.body = "Please find the attached git report."

    def email_report(self, attach_file_name, table_html):
        msg = MIMEMultipart()
        msg['From'] = self.sender_addr
        msg['To'] = self.recipients
        msg['Subject'] = self.subject

        msg.attach(MIMEText(table_html, 'html'))

        for f in attach_file_name:

            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(("outputs/" + str(f)), "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=%s' %f)
            msg.attach(part)
            pass

        server = smtplib.SMTP(self.sender_smtp_serv, self.sender_smtp_serv_port)
        server.starttls()
        server.login(self.sender_addr, self.sender_pass)
        server.sendmail(self.sender_addr, self.recipients, msg.as_string())
        server.quit()
        pass