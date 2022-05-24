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

    #if isHeadless: option.add_argument('--headless')
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
    for tr in table_row:
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
   
#  /content/travel/en/traveladvisories/traveladvisories/netherlands-travel-advisory.html

def get_scraped_table_data(data, driver):
    data_list=[]
    for i in data:
        print(i['link'])
        link = i['link']
        driver.get(f'https://travel.state.gov{link}')
        time.sleep(1)
        text_data = driver.find_elements_by_css_selector('div.tsg-rwd-emergency-alert-text')[0].text
        i['information'] = text_data
        data_list.append(i)
    return data_list


def canadian_website_load_page(driver):
    driver.get('https://travel.gc.ca/travelling/advisories')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "lxml")
    table_row = soup.select('#reportlist > tbody > tr > td > a')
    return table_row

def get_anchor_Links_of_canadian_website(table_row,driver):
    data = []
    for tr in table_row:
        link = tr.get('href')
        page_url = f"https://travel.gc.ca{link}"
        print(page_url)
        
        driver.get(page_url)
        
        
        #country-name text
        h1 = driver.find_element_by_css_selector('h1#wb-cont')
        country_name = ' '.join(h1.text.split(' ')[:-2])
        
        #canadian_key_encode
        
        canadian_key_encode = base64.b64encode(country_name.encode()).decode()
        
        #travel-alert
        span_alert = driver.find_element_by_css_selector('span#riskLevelBanner')
        alert_text = span_alert.text
        
        
        #Update fate and Time
        span_update_date_and_time = driver.find_element_by_css_selector('span#lastUpdateDateLbl')
        last_updated = span_update_date_and_time.text
        
        
        #Risk link title
        risk_title = driver.find_element_by_css_selector('span#title-risk')
        risk_heading = risk_title.text
        
        
        #Risk link text
        risk_body_text = driver.find_element_by_css_selector('div#risk')
        risk_information = risk_body_text.text
        
        
        #security link text
        security_of_country =  driver.find_element_by_css_selector('div#security')
        country_security = security_of_country.text
        
        
        #entry and exit procedure link text
        entry_exit =  driver.find_element_by_css_selector('div#entryexit')
        criteria = entry_exit.text
        
        #health link text
        health_div =  driver.find_element_by_css_selector('div#health')
        health = health_div.text
        
        #laws text
        law_div =  driver.find_element_by_css_selector('div#laws')
        laws = law_div.text
        
        #natural-disaster text
        natural_disaster_div =  driver.find_element_by_css_selector('div#disasters')
        natural_disaster = natural_disaster_div.text
        
        #sending data to data list according to tables
        data.append(
           {'country_name': country_name, "alert_text":alert_text, 'last_updated':last_updated, 'risk_heading':risk_heading, 'risk_information': risk_information, 'country_security':country_security, 'criteria':criteria, 'health':health, 'laws':laws, 'natural_disaster':natural_disaster, 'canadian_key_encode':canadian_key_encode}
         )
    return data

# def get_scraped_table_data_of_canadian_website(data):
#     data_list=[]
#     for i in data:
#         # print(i['country_name'])
#         # print(i['alert_text'])
#         # print(i['last_updated'])
#         # print(i['risk_heading'])
#         # time.sleep(1)
#         data_list.append(i)
#     return data_list



