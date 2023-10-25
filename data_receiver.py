from typing import List
from flask import Flask, request
from dacite import from_dict
from dataclasses import dataclass
import yaml
import datetime
import sys
import time
from datetime import timedelta
import mysql.connector

@dataclass
class Measurment_model:
    timestamp:int
    sensor_id:int
    m5: int
    m15: int
    m30: int
    h1: int
    h4: int
    d1: int
    temperature: float
    humidity:float

@dataclass
class Measurments_model:
    measurments: List[Measurment_model]

class MeasurmentSaver(object):
    
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.mydb = None
     
    def __enter__(self):
        try:
            self.mydb = mysql.connector.connect(host='localhost',
                                       user=self.user,
                                       password=self.password,
                                       database = 'monitor')
            print('Connected to DB')
        except Exception as error:
            print(error)     
        return self.save
 
    def __exit__(self, *args):
        if self.mydb == None:
            print('Error! Can not close connection to DB')
            return
        
        self.mydb.close() 
        print('DB connection is closed')

    def save(self, measurments:Measurments_model):
        if self.mydb == None:
            print('Error! Can not store to DB')
            return

        mycursor = self.mydb.cursor()

        for measurment in measurments.measurments:

            sql = """INSERT INTO measurings 
                        (timestamp,
                        sensor_id,
                        m5,
                        m15,
                        m30,
                        h1,
                        h4,
                        d1,
                        temperature,
                        humidity) 
                    VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE temperature = %s, humidity = %s"""
            
            val = (measurment.timestamp, 
                measurment.sensor_id,
                measurment.m5,
                measurment.m15,
                measurment.m30,
                measurment.h1,
                measurment.h4,
                measurment.d1,
                measurment.temperature,
                measurment.humidity,
                measurment.temperature,
                measurment.humidity)
            
            mycursor.execute(sql, val)

        self.mydb.commit()

app = Flask(__name__)

@app.post('/update')
def update_post():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            json = request.json
            measurments = from_dict(data_class=Measurments_model, data=json)
            print(measurments)

            with open('config.yaml', 'r') as file:
                config = yaml.safe_load(file)

            db_user = config['db_user']
            db_password = config['db_password']
    
            with MeasurmentSaver(db_user, db_password) as save:
                save(measurments) 

            return 'Ok', 200
        except Exception as error:
            print(error)   
            return str(error), 500
    else:
        return 'Content-Type not supported!', 500