import asyncio
import datetime
import os
from decouple import config
from sqlalchemy import Table
from sqlalchemy.sql import text

from database import Base, SessionLocal, engine

def insert_data(data=None):
    
    sess = SessionLocal()
    with sess.connection() as con:
    
        if data is None:
            print("data is missing to inesrt")
            return None
        elif (data):
            return data
        
        #statement = text("INSERT INTO travel_db.alert_info (country_name, travel_alerts, status_date, link, information, key_encode) VALUES (:country_name, :travel_alerts, :status_date, :link, :information, :key_encode)")
        #statement = text("INSERT INTO travel_db.alert_info (country_name, travel_alerts, status_date, link, information, key_encode ) VALUES (:country_name, :travel_alerts, :status_date, :link, :information, :key_encode) ON DUPLICATE KEY UPDATE travel_alerts = travel_alerts, status_date = status_date, information = information")

    statement = text("INSERT INTO travel_db.alert_info (country_name, travel_alerts, status_date, link, information, key_encode ) VALUES (:country_name, :travel_alerts, :status_date, :link, :information, :key_encode) ON DUPLICATE KEY UPDATE travel_alerts = travel_alerts, status_date = status_date, information = information")   
    con.execute(statement, data)
    print("please wait inserting data")

