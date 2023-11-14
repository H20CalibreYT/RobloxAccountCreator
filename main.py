import secrets
import string
import time
import os
import sys
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests

def status(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + text + "\033[0m")

#Config
Accounts = 999999 #how many accounts

# URLs
first_names_url = "https://raw.githubusercontent.com/H20CalibreYT/RobloxAccountCreator/main/firstnames.txt"
last_names_url = "https://raw.githubusercontent.com/H20CalibreYT/RobloxAccountCreator/main/lastnames.txt"
roblox_url = "https://www.roblox.com/"

status("Getting first names...")
first_names_response = requests.get(first_names_url)
status("Getting last names...")
last_names_response = requests.get(last_names_url)

# Check if name loading was successful
if first_names_response.status_code == 200 and last_names_response.status_code == 200:
    first_names = list(set(first_names_response.text.splitlines()))
    last_names = list(set(last_names_response.text.splitlines()))
else:
    status("Name loading failed. Re-Execute the script.")
    sys.exit()

# File paths
files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
text_files_folder = os.path.join(files_path, "Accounts")
text_file = os.path.join(text_files_folder, f"Accounts_{date.today()}.txt")
text_file2 = os.path.join(text_files_folder, f"AltManagerLogin_{date.today()}.txt")

# Create folder if it does not exist
if not os.path.exists(text_files_folder):
    os.makedirs(text_files_folder)

# Lists of days, months and years
days = [str(i + 1) for i in range(10, 28)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(i + 1) for i in range(1980, 2004)]

# Password generator
def gen_password(length):
    status("Generating a password...")
    chars = string.ascii_letters + string.digits + "Ññ¿?¡!#$%&/()=\/¬|°_-[]*~+"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

#Username generator
def gen_user(first_names, last_names):
    status("Generating a username...")
    first = secrets.choice(first_names)
    last = secrets.choice(last_names)
    full = f"{first}{last}_{secrets.choice([i for i in range(1, 999)]):03}"
    return full

def create_account(url, first_names, last_names):
    try:
        status("Starting to create an account...")
        cookie_found = False
        username_found = False
        elapsed_time = 0

        status("Initializing webdriver...")
        driver = webdriver.Edge()
        driver.set_window_size(1200, 800)
        driver.set_window_position(0, 0)
        driver.get(url)
        time.sleep(2)

        # HTML items
        status("searching for items on the website")
        username_input = driver.find_element("id", "signup-username")
        username_error = driver.find_element("id", "signup-usernameInputValidation")
        password_input = driver.find_element("id", "signup-password")
        day_dropdown = driver.find_element("id", "DayDropdown")
        month_dropdown = driver.find_element("id", "MonthDropdown")
        year_dropdown = driver.find_element("id", "YearDropdown")
        male_button = driver.find_element("id", "MaleButton")
        female_button = driver.find_element("id", "FemaleButton")
        register_button = driver.find_element("id", "signup-button")

        status("Selecting day...")
        Selection = Select(day_dropdown)
        Selection.select_by_value(secrets.choice(days))
        time.sleep(0.3)

        status("Selecting month...")
        Selection = Select(month_dropdown)
        Selection.select_by_value(secrets.choice(months))
        time.sleep(0.3)

        status("Selecting year...")
        Selection = Select(year_dropdown)
        Selection.select_by_value(secrets.choice(years))
        time.sleep(0.3)

        while not username_found:
            status("Selecting username...")
            username = gen_user(first_names, last_names)
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)
            if username_error.text.strip() == "":
                username_found = True
        
        status("Selecting password...")
        password = gen_password(25)
        password_input.send_keys(password)
        time.sleep(0.3)

        status("Selecting gender...")
        gender = secrets.choice([1,2])
        if gender == 1:
            male_button.click()
        else:
            female_button.click()
        time.sleep(0.5)

        status("Registering account...")
        register_button.click()
        time.sleep(3)

        # Wait until the account creation limit is reset
        try:
            driver.find_element("id", "GeneralErrorText")
            driver.quit()
            for i in range(360):
                status(f"Limit reached, waiting... {i+1}/{360}")
                time.sleep(1)
        except:
            pass

        # Wait until the cookie is found or the maximum time has passed
        while not cookie_found and elapsed_time < 180:
            status("Waiting for the cookie...")
            time.sleep(3)
            elapsed_time += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    cookie_found = True
                    break
        if cookie_found:
            status("Cookie found...")
            return [cookie.get('value'), username, password]

    except Exception as e:
        pass
    finally:
        pass

# Save account information to text file
def save_account_info(account_info):
    status("Saving account info...")
    with open(text_file, 'a') as file:
        file.write(f"Username: {account_info[1]}\nPassword: {account_info[2]}\nCookie: {account_info[0]}\n\n\n")

# Save login information for AltManager
def save_altmanager_login(account_info):
    with open(text_file2, 'a') as file:
        status("Saving account login (for alt manager)...")
        file.write(f"{account_info[1]}:{account_info[2]}\n")

# Create accounts
for _ in range(Accounts):
    account = create_account(roblox_url, first_names, last_names)
    if account is not None:
        save_account_info(account)
        save_altmanager_login(account)
        status("Successfully created!")
        time.sleep(3)
