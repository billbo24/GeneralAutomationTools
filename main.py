


#ojiu dhpl epcq tuwb 

#%%
import smtplib
from email.mime.text import MIMEText


# Gmail credentials
EMAIL_ADDRESS = "wfloyd1231@gmail.com"
APP_PASSWORD = "ojiudhplepcqtuwb"  # From Step 1

def send_email(to_email, subject, body):
    # Create email
    msg = MIMEText(body)
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    # Connect to Gmail SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, APP_PASSWORD)
        smtp.send_message(msg)



if __name__ == "__main__":
    send_email("william.floyd@kleingers.com", "Test Email", "This is a test from Python!")
    print("Email sent successfully!")



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


send_email(subject, body, sender, recipients, password)

# %%
