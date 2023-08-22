import argparse, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PORT_NUMBER = 465
argparser = argparse.ArgumentParser()
argparser.add_argument("-n", "--name", help="Name of file for email attachment", required=True)
argparser.add_argument("-e", "--email", help="Email to send information", required=True)

args = argparser.parse_args()
file_name = args.name
receiver_email = args.email

subject = "hb_read_server: Session Data Attached"
body = "This email has the attached data from the previous session that you concluded."
sender = "uclalemurbiometrics@gmail.com"
password = "fswscygbiobkxxmn"

message = MIMEMultipart()
message["From"] = sender
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, 'plain'))

path_to_file = "./data/" + file_name
part = MIMEBase("application", "octet-stream")
with open(path_to_file, "rb") as file:
    part.set_payload(file.read())

encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment; filename= %s" % file_name)

message.attach(part)
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", PORT_NUMBER, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver_email, text)