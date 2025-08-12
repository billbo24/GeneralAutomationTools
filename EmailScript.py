

#%%

import smtplib
from email.mime.text import MIMEText
import time 

subject = "Email Subject"
body = "This is the body of the text message"
sender = "wfloyd1231@gmail.com"
recipients = ["billbo24@aol.com"]
password = "ojiudhplepcqtuwb"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.set_debuglevel(1)  # <--- Enable debug output
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
       print("ALRIGHT JUST HIT THE SEND")
       time.sleep(3)


    print("Message sent!")


#send_email(subject, body, sender, recipients, password)
