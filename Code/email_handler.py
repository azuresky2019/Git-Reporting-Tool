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
        with open('config/config.json', 'rb') as email_file:
            user_email_raw = json.load(email_file)
            email_file.close()
        self.recipients = user_email_raw['email']
        self.subject = "Git report"
        self.body = "Please find the attached git report."

    def email_report(self, attach_file_name, table_html):
        msg = MIMEMultipart()
        msg['From'] = self.sender_addr
        msg['To'] = self.recipients
        msg['Subject'] = self.subject


        msg.attach(MIMEText(table_html, 'html'))

        # Single attachment
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attach_file_name, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=%s' %attach_file_name)
        msg.attach(part)

        '''
        # For Multiple attachments 
        
        for f in attach_file_name:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(("outputs/" + str(f)), "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=%s' %f)
            msg.attach(part)
            pass
        '''

        server = smtplib.SMTP(self.sender_smtp_serv, self.sender_smtp_serv_port)
        server.starttls()
        server.login(self.sender_addr, self.sender_pass)
        server.sendmail(self.sender_addr, self.recipients, msg.as_string())
        server.quit()
        pass

    def error_email(self):

        body_text = "<h4>Error Notification!</h4>" \
                    "<p>Hi!</p>" \
                    "<p>This is to notify you that the <b>Git Report Tool</b> encountered an error while generating " \
                    "and sending report.</p>" \
                    "<i>This is an automatically generated email, please do not reply.</i>"

        msg = MIMEMultipart()
        msg['From'] = self.sender_addr
        msg['To'] = self.recipients
        msg['Subject'] = self.subject

        msg.attach(MIMEText(body_text, 'html'))

        server = smtplib.SMTP(self.sender_smtp_serv, self.sender_smtp_serv_port)
        server.starttls()
        server.login(self.sender_addr, self.sender_pass)
        server.sendmail(self.sender_addr, self.recipients, msg.as_string())
        server.quit()
        pass