import asyncio
import datetime
import os
from decouple import config
from sqlalchemy import Table
from sqlalchemy.sql import text

from database import Base, SessionLocal, engine
#another function for Canadaian advisory
def insert_data_usa_website(data=None):
    
    sess = SessionLocal()
    with sess.connection() as con:
    
        if data is None:
            print("data is missing to inesrt")
            return 
        
        #statement = text("INSERT INTO travel_db.alert_info (country_name, travel_alerts, status_date, link, information, key_encode) VALUES (:country_name, :travel_alerts, :status_date, :link, :information, :key_encode)")
        #statement = text("INSERT INTO travel_db.alert_info (country_name, travel_alerts, status_date, link, information, key_encode ) VALUES (:country_name, :travel_alerts, :status_date, :link, :information, :key_encode) ON DUPLICATE KEY UPDATE travel_alerts = travel_alerts, status_date = status_date, information = information")

        statement = text("INSERT INTO travel_db.travel_info (country_name, travel_alerts, status_date, link, information, key_encode ) VALUES (:country_name, :travel_alerts, :status_date, :link, :information, :key_encode) ON DUPLICATE KEY UPDATE travel_alerts = travel_alerts, status_date = status_date, information = information")   
        con.execute(statement, data)
        print("please wait inserting data")

def insert_data_canadian_website(data=None):
    
    sess = SessionLocal()
    with sess.connection() as con:
        
        if data is None:
            print("data is missing to insert")
            return
        
        statement = text("INSERT INTO travel_db.canadian_travel_info (country_name, alert_text, last_updated, risk_heading, risk_information, country_security, criteria, health, laws, natural_disaster, canadian_key_encode ) VALUES (:country_name, :alert_text, :last_updated, :risk_heading, :risk_information, :country_security, :criteria, :health, :laws, :natural_disaster, :canadian_key_encode) ON DUPLICATE KEY UPDATE alert_text = alert_text, last_updated = last_updated, risk_heading = risk_heading, risk_information = risk_information, country_security = country_security, criteria = criteria, health = health")
        con.execute(statement, data)
        print("please wait inserting data")