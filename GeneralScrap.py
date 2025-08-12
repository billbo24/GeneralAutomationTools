
#%% Just a general testing and scrap file
import requests


url = "https://billbo24.pythonanywhere.com/email"

payload = {"Subject": "hello world"
           ,'From':'wfloyd1231@gmail.com'
           ,'To':'william.floyd@kleingers.com'
           ,'Body':'Hey Billy it was a pleasure getting lunch with you today 2:29PM'
           ,'Password':'ojiudhplepcqtuwb'}  # Must be under the key "body"


#url = "https://billbo24.pythonanywhere.com/webhook"

#payload = {"body": "hello world"}  # Must be under the key "body"



response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())  # {'uppercase_body': 'HELLO WORLD'}
# %%
