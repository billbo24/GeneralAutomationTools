
#%%
#Looking to get some practice in with selenium
#Might be able to run the "give everyone their SMRFs" part of the process

# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Adjust this path to where your chromedriver.exe is
service = Service(r"C:\Users\wfloyd\OneDrive - The Kleingers Group\Documents\ChromeDriver\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.python.org")
print(driver.title)

driver.implicitly_wait(5)

search_bar = driver.find_element(By.ID,"id-search-field")

search_bar.clear()

search_bar.send_keys("getting started with python")

search_bar.send_keys(Keys.RETURN)

# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


email = 'vjfheeeviusdhfg@gmail.com'
full_name = 'Dingle Jones'


# Specify the path to ChromeDriver
service = Service(r"C:\Users\wfloyd\OneDrive - The Kleingers Group\Documents\ChromeDriver\chromedriver-win64\chromedriver.exe")

# Step 1: launch the browser
driver = webdriver.Chrome(service=service)
print("Browser launched successfully!")

#2: navigate to page
driver.get("http://automationexercise.com/")
print("Navigated to http://automationexercise.com/")

# Verify that the home page is visible
expected_title = "Automation Exercise"  # Replace with the actual title of the home page
if driver.title == expected_title:
    print("Home page is visible!")
else:
    print("Home page is not visible. Current title:", driver.title)


# Click on 'Signup/Login' button
signup_login_button = driver.find_element(By.LINK_TEXT, "Signup / Login")  # Replace with the actual text or locator
signup_login_button.click()
print("'Signup/Login' button clicked!")

# Wait for the "New User Signup" section to be visible
try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    new_user_signup = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='New User Signup!']")))  # Replace with the actual locator
    print("New User Signup is visible!")
except:
    print("New User Signup is not visible.")


#Enter name and email address
name_field = driver.find_element(By.NAME, "name")  # Replace 'name' with the actual name attribute of the input field
email_field = driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")  # Replace with the actual locator

name_field.send_keys(f"{full_name}")  # Replace with the desired name
email_field.send_keys(f"{email}")  # Replace with the desired email
print("Entered name and email address!")


# Step 7: Click 'Signup' button
signup_button = driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")  # Replace with the actual locator
signup_button.click()
print("'Signup' button clicked!")


# Step 8: Verify 'ENTER ACCOUNT INFORMATION' is visible
try:
    enter_account_info = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Enter Account Information']")))  # Replace with the actual locator
    print("'ENTER ACCOUNT INFORMATION' is visible!")
except:
    print("'ENTER ACCOUNT INFORMATION' is not visible.")



# Step 9: Fill details
# Select Title (e.g., Mr.)
title_radio_button = driver.find_element(By.ID, "id_gender1")  # Replace with the actual ID of the radio button
title_radio_button.click()

# Fill in Name (already pre-filled, but you can verify or modify if needed)
name_field = driver.find_element(By.ID, "name")  # Replace with the actual ID
name_field.clear()
name_field.send_keys(f"{full_name}")  # Replace with the desired name

# Fill in Email (already pre-filled, but you can verify or modify if needed)
#email_field = driver.find_element(By.ID, "email")  # Replace with the actual ID
#email_field.clear()
#email_field.send_keys(f"{email}")  # Replace with the desired email

# Fill in Password
password_field = driver.find_element(By.ID, "password")  # Replace with the actual ID
password_field.send_keys("securepassword123")  # Replace with the desired password

# Select Date of Birth
day_dropdown = driver.find_element(By.ID, "days")  # Replace with the actual ID
day_dropdown.send_keys("10")  # Replace with the desired day

month_dropdown = driver.find_element(By.ID, "months")  # Replace with the actual ID
month_dropdown.send_keys("May")  # Replace with the desired month

year_dropdown = driver.find_element(By.ID, "years")  # Replace with the actual ID
year_dropdown.send_keys("1990")  # Replace with the desired year

print("Filled in account details!")



# Step 10: Select checkbox 'Sign up for our newsletter!'
newsletter_checkbox = driver.find_element(By.ID, "newsletter")  # Replace with the actual ID
newsletter_checkbox.click()
print("Selected 'Sign up for our newsletter!' checkbox!")


# 11. Select checkbox 'Receive special offers from our partners!'
newsletter_checkbox = driver.find_element(By.ID, "optin")  # Replace with the actual ID
newsletter_checkbox.click()
print("Selected 'Receive special offers from our partners!' checkbox!")

def find_field_and_enter_info(driver,ID_value,enter_value):
    # Fill in first name
    name_field = driver.find_element(By.ID, ID_value)  # Replace with the actual ID
    name_field.clear()
    name_field.send_keys(enter_value)  # Replace with the desired name



find_field_and_enter_info(driver,'first_name','Dingle')
find_field_and_enter_info(driver,'last_name','Jones')
find_field_and_enter_info(driver,'company','Wendy\'s')
find_field_and_enter_info(driver,'address1','123 Main Street')

month_dropdown = driver.find_element(By.ID, "country")  # Replace with the actual ID
month_dropdown.send_keys("United States")  # Replace with the desired month

find_field_and_enter_info(driver,'state','New Jersey')
find_field_and_enter_info(driver,'city','Ridgewood')
find_field_and_enter_info(driver,'zipcode','07450')
find_field_and_enter_info(driver,'mobile_number','201-867-5309')





#12, fill additional details
# Fill in first name
'''
name_field = driver.find_element(By.ID, "first_name")  # Replace with the actual ID
name_field.clear()
name_field.send_keys("Dingle")  # Replace with the desired name

name_field = driver.find_element(By.ID, "last_name")  # Replace with the actual ID
name_field.clear()
name_field.send_keys("Jones")  # Replace with the desired name
'''


# Click on 'Create Account' button
create_account = driver.find_element(By.XPATH, "//button[@data-qa='create-account']")
create_account.click()
print("Create account button clicked!")



# Wait for the Account created! to appears
try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    account_created = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-created']")))
    print("Account Created is visible!")
except:
    print("Account Created is not visible.")


# Click on continue button
continue_button = driver.find_element(By.XPATH, "//a[@data-qa='continue-button']")
continue_button.click()
print("Continue button clicked!")


#f"{full_name}"
# Verify that Logged in as username is available
try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    logged_in_as = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), ' Logged in as ')]")))
    print("Successfully Logged in")
except:
    print("Not logged in")


# Click on delete button
delete_button = driver.find_element(By.XPATH, "//a[@href='/delete_account']")
delete_button.click()
print("Delete button clicked!")


# Wait for the Account created! to appears
try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    account_created = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-deleted']")))
    print("Account Deleted is visible!")
except:
    print("Account Deleted is not visible.")


# Click on continue button
continue_button = driver.find_element(By.XPATH, "//a[@data-qa='continue-button']")
continue_button.click()
print("Continue button clicked!")

# %%
