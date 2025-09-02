

#%% Listener script
import imaplib, email, requests, time



IMAP_SERVER = "imap.gmail.com"
EMAIL = "wfloyd1231@gmail.com"
PASSWORD = "ojiudhplepcqtuwb"
POST_URL = 'https://billbo24.pythonanywhere.com/email'
KEYWORD = 'banana'



def check_inbox():
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")
    status, messages = imap.search(None, "UNSEEN")

    for num in messages[0].split():
        _, data = imap.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        subject = msg["Subject"] or ""
        sender = msg["From"]

        # skip if keyword not in subject
        if KEYWORD not in subject:
            continue

        # extract body text
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        
        payload = {
            "Subject": "Requested text",
            "Body": body,
            "To": "billbo24@aol.com",
            "Password":PASSWORD,
            "From":"wfloyd1231@gmail.com"
        }

        response = requests.post(POST_URL, json=payload)

        print(response.status_code)
        print(response.json())

    imap.close()
    imap.logout()

# Loop forever, checking every 60s
for i in range(5):
    print(f"polling inbox time {i}")
    check_inbox()
    time.sleep(5) #poll every 5 seconds
# %%
