import os
import re
import time

import asyncio

# import wget
# from bs4 import BeautifulSoup
# from decouple import config
import base64
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
from models import insert_data
from decouple import config
from config import get_env
# from fastapi import HTTPException


# from bs4 import BeautifulSoup
# from decouple import config



# from fastapi import HTTPException

try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
except:
    pass

app_config = get_env()


def load_driver_properties():
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])

    # if isHeadless: option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-popup-blocking")
    option.add_argument('--disable-dev-shm-usage')
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    
    if app_config.ENV == 'development':
        print('loading local chrome driver...', os.path.realpath('chromedriver/chromedriver'))
        driver = webdriver.Chrome(executable_path=os.path.realpath('chromedriver/chromedriver.exe'), options=option, desired_capabilities=caps)
        print('local driver is running')
    
        return driver
    
    if app_config.ENV == 'testing':
        driver = webdriver.Remote(
            options=option, 
            desired_capabilities=caps,
            command_executor=f'http://{app_config.SELENIUM_URL}:4444/wd/hub'
        )
        return driver


def load_page(driver):
    driver.get('https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "lxml")
    table_row = soup.select('#tableNum_1 > div > table > tbody > tr.rowDisplay')
    
    return table_row
def get_anchor_Links(table_row):
    data = []
    for tr in table_row[0:3]:
        td_list = tr.find_all('td')
        link = td_list[0].find('a').get('href')
        country_name = td_list[0].text
        travel_alerts = td_list[1].text
        status_date =  td_list[2].text
        country_name_only = ' '.join(country_name.split(' ')[:-2])
        key_encode = base64.b64encode(country_name_only.encode()).decode()
        data.append(
            {'country_name': country_name, "travel_alerts":travel_alerts, 'status_date':status_date, 'link':link, 'key_encode': key_encode}
        )
    return data
   


def get_scraped_table_data(data, driver):
    data_list=[]
    for i in data[0:3]:
        print(i['link'])
        link = i['link']
        driver.get(f'https://travel.state.gov{link}')
        time.sleep(1)
        text_data = driver.find_elements_by_css_selector('div.tsg-rwd-emergency-alert-text')[0].text
        i['information'] = text_data
        data_list.append(i)
    return data_list
