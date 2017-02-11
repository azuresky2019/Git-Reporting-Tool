import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

class Email:
    def __init__(self):
        self.sender_addr = "tech_temco@outlook.com"
        self.sender_pass = ""
        self.sender_smtp_serv = "smtp.live.com"
        self.sender_smtp_serv_port = 587
        self.recipients = list(["maurice@temcocontrols.com", "er.rajuregmi@gmail.com"])
        self.subject = "Weekly Git report"
        self.body = "Please find the attached git report."

    def email_report(self, attach_file_path, attach_file_name, table_html):
        msg = MIMEMultipart()
        msg['From'] = self.sender_addr
        msg['To'] =  ", ".join(self.recipients)
        # msg['To'] = self.recipients
        msg['Subject'] = self.subject

        part = MIMEBase('application', "octet-stream")

        msg.attach(MIMEText(table_html, 'html'))

        part.set_payload(open(attach_file_path, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=%s' %attach_file_name)
        msg.attach(part)

        server = smtplib.SMTP(self.sender_smtp_serv, self.sender_smtp_serv_port)
        server.starttls()
        server.login(self.sender_addr, self.sender_pass)
        server.sendmail(self.sender_addr, self.recipients, msg.as_string())
        server.quit()
        pass