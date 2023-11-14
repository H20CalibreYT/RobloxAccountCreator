import secrets
import string
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date
import requests

git = "https://raw.githubusercontent.com/H20CalibreYT/RobloxAccountCreator/main/"
FNurl = git+"firstnames.txt"
LNurl = git+"lastnames.txt"

FNResponse = requests.get(FNurl)
LNResponse = requests.get(LNurl)

if FNResponse.status_code == 200 and LNResponse.status_code == 200:
    FirstNames = list(set(FNResponse.text.splitlines()))
    LastNames = list(set(LNResponse.text.splitlines()))
else:
    print("Name loading failed, re-execute or something idk")
    sys.exit()

FilesPath = os.path.dirname(os.path.abspath(sys.argv[0]))
TextFilesFolder = os.path.join(FilesPath,"Accounts")
TextFile = os.path.join(TextFilesFolder,"Accounts"+str(date.today())+".txt")
TextFile2 = os.path.join(TextFilesFolder,"AltManagerLogin"+str(date.today())+".txt")

if not os.path.exists(TextFilesFolder):
    os.makedirs(TextFilesFolder)

Days = [str(i+1) for i in range(10,28)]
Months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
Years = [str(i+1) for i in range(1980, 2004)]

def GenPassword(lenght):
    chars = string.ascii_letters + string.digits + "Ññ¿?¡!#$%&/()=\/¬|°_-[]*~+"
    password = ''.join(secrets.choice(chars) for i in range(lenght))
    return password

def GenUser():
    first = secrets.choice(FirstNames)
    last = secrets.choice(LastNames)
    Full = first+last+"_"+str(secrets.choice([i for i in range(1,999)])).zfill(3)
    return Full

def CreateAcc(url):
    try:
        CookieFound = False
        UsernameFound = False
        ElapsedTime = 0

        driver = webdriver.Edge()
        driver.set_window_size(1200, 800)
        driver.set_window_position(0,0)
        driver.get(url)
        time.sleep(2)
        username_input = driver.find_element("id", "signup-username")
        username_error = driver.find_element("id", "signup-usernameInputValidation")
        password_input = driver.find_element("id", "signup-password")
        day_dropdown = driver.find_element("id", "DayDropdown")
        month_dropdown = driver.find_element("id", "MonthDropdown")
        year_dropdown = driver.find_element("id", "YearDropdown")
        sex_button = driver.find_element("id", "MaleButton")
        register_button = driver.find_element("id","signup-button")
        Selection = Select(day_dropdown)
        Selection.select_by_value(secrets.choice(Days))
        time.sleep(0.3)

        Selection = Select(month_dropdown)
        Selection.select_by_value(secrets.choice(Months))
        time.sleep(0.3)

        Selection = Select(year_dropdown)
        Selection.select_by_value(secrets.choice(Years))
        time.sleep(0.3)

        while not UsernameFound:
            Username = GenUser()
            username_input.clear()
            username_input.send_keys(Username)
            time.sleep(1)
            if username_error.text.strip() == "":
                UsernameFound = True
        
        Password = GenPassword(25)
        password_input.send_keys(Password)
        time.sleep(0.3)

        sex_button.click()
        time.sleep(0.5)

        register_button.click()
        time.sleep(3)

        try:
            driver.find_element("id","GeneralErrorText")
            driver.quit()
            print("IN COOLDOWN")
            for i in range(360):
                print(f"in cooldown {i+1}/{360}")
                time.sleep(1)
        except:
            print()
        
        while (not CookieFound) and (ElapsedTime < 180):
            time.sleep(3)
            ElapsedTime += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    CookieFound = True
                    break
        if CookieFound:
            return [cookie.get('value'),Username,Password]
        
    except Exception as e:
        print("Ignore me",e)
    finally:
        print("Ignore me too")

def save_account_info(account_info):
    with open(TextFile, 'a') as file:
        file.write(f"Username: {account_info[1]}\nPassword: {account_info[2]}\nCookie: {account_info[0]}\n\n\n")

def save_altmanger_login(account_info):
    with open(TextFile2, 'a') as file:
        file.write(f"{account_info[1]}:{account_info[2]}\n")

for i in range(999999):
    Account = CreateAcc("https://www.roblox.com/")
    if Account != None:
        save_account_info(Account)
        save_altmanger_login(Account)
        time.sleep(3)
