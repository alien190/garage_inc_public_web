from .temperatures import temperatures_from_json
from .airflows import airflows_from_json
from flask import (Blueprint, request)
from .db import get_db

bp = Blueprint('update_data', __name__, url_prefix='/update_data')

@bp.route('/temperatures/', methods=['POST'])
def update_temperautres():
    try:
        db = get_db()
        json = request.json
        temperatures = temperatures_from_json(json)
        
        for temperature in temperatures.values:

                sql = """INSERT INTO temperatures 
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
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                        ON CONFLICT(timestamp, sensor_id) DO UPDATE SET temperature = ?, humidity = ?"""
                
                val = (temperature.timestamp, 
                    temperature.sensor_id,
                    temperature.m5,
                    temperature.m15,
                    temperature.m30,
                    temperature.h1,
                    temperature.h4,
                    temperature.d1,
                    temperature.temperature,
                    temperature.humidity,
                    temperature.temperature,
                    temperature.humidity)
                
                db.execute(sql, val)

        db.commit()
        return 'Data was updated', 200

    except Exception as error:
        print(error)
        return str(error), 500
    

@bp.route('/airflows/', methods=['POST'])
def update_airflows():
    try:
        db = get_db()
        json = request.json
        values = airflows_from_json(json)
        
        for value in values.values:

                sql = """INSERT INTO airflows
                            (timestamp,
                            sensor_id,
                            m5,
                            m15,
                            m30,
                            h1,
                            h4,
                            d1,
                            air_flow_rate,
                            temperature,
                            air_consumption) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                        ON CONFLICT(air_flow_rate, temperature, air_consumption) DO UPDATE SET air_flow_rate = ?, temperature = ?, air_consumption = ?"""
                
                val = (value.timestamp, 
                    value.sensor_id,
                    value.m5,
                    value.m15,
                    value.m30,
                    value.h1,
                    value.h4,
                    value.d1,
                    value.air_flow_rate,
                    value.temperature,
                    value.air_consumption,
                    value.air_flow_rate,
                    value.temperature,
                    value.air_consumption)
                
                db.execute(sql, val)

        db.commit()
        return 'Data was updated', 200

    except Exception as error:
        print(error)
        return str(error), 500