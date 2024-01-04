from .retro_temperatures import retro_temperatures_from_rows
from .retro_airflows import retro_airflows_from_rows
from flask import (Blueprint, json, Request, request)
from .db import get_db
from pythonping import ping

allowed_periods = ['m1', 'm5', 'm15', 'm30', 'h1', 'h4', 'd1']

bp = Blueprint('get_data', __name__, url_prefix='/get_data')

def get_sensor_id(rq:Request):
    sensor_id = request.args.get('sensor_id')
    if not sensor_id:
        return 0
    return int(sensor_id)

@bp.route('/temperatures_retro/', methods=['GET'])
def get_temperatures_retro():
    return get_retro(request, 0)

@bp.route('/airflows_retro/', methods=['GET'])
def get_airflows_retro():
    return get_retro(request, 1)

def get_retro(request:Request, type:int ):
    try:
        sensor_id = get_sensor_id(request)
        if sensor_id == 0:
           error = 'sensor_id parameter error'
           print(error)
           return error, 500
        
        db = get_db()
        period = request.args.get('period', 'm1')
        sql = ""
        if(type == 0): 
            sql = get_temperatures_sql(period, sensor_id)
        if(type == 1): 
            sql = get_airflows_sql(period, sensor_id)    
        cursor = db.execute(sql)
        rows = cursor.fetchall()
        if type == 0:
            measurments = retro_temperatures_from_rows(rows)
            return json.dumps(measurments.__dict__), 200
        if type == 1:
            measurments = retro_airflows_from_rows(rows)
            return json.dumps(measurments.__dict__), 200

    except Exception as error:
        print(error)
        return str(error), 500

def get_temperatures_sql(period:str, sensor_id:int):
    period = period.lower()
    
    if not period in allowed_periods:
        period = 'm1'
    
    if(period == 'm1'):
        return f'''SELECT timestamp,temperature,humidity,sensor_id 
                  FROM temperatures 
                  WHERE sensor_id = {sensor_id}
                  ORDER BY timestamp DESC
                  LIMIT 100'''

    
    return f'''SELECT {period} as timestamp, 
                     avg(temperature) as temperature, 
                     avg(humidity) as humidity,
                     sensor_id
               FROM temperatures 
               WHERE sensor_id = {sensor_id}
               GROUP BY {period}
               ORDER BY timestamp DESC
               LIMIT 100'''

def get_airflows_sql(period:str, sensor_id:int):
    period = period.lower()
    
    if not period in allowed_periods:
        period = 'm1'
    
    if(period == 'm1'):
        return f'''SELECT timestamp,air_flow_rate,temperature,air_consumption,sensor_id 
                  FROM airflows
                  WHERE sensor_id = {sensor_id}
                  ORDER BY timestamp DESC
                  LIMIT 100'''

    
    return f'''SELECT {period} as timestamp, 
                     avg(air_flow_rate) as air_flow_rate, 
                     avg(temperature) as temperature,
                     avg(air_consumption) as air_consumption,
                     sensor_id
               FROM airflows 
               WHERE sensor_id = {sensor_id}
               GROUP BY {period}
               ORDER BY timestamp DESC
               LIMIT 100'''
    
@bp.route('/temperatures_last_timestamp/', methods=['GET'])
def get_temperatures_last_timestamp():
    return get_last_timestamp(request, "temperatures")
    
@bp.route('/airflows_last_timestamp/', methods=['GET'])
def get_airflows_last_timestamp():
    return get_last_timestamp(request, "airflows")
    
def get_last_timestamp(request:Request, table_name:str):
    try:
        sensor_id = get_sensor_id(request)
        if sensor_id == 0:
           error = 'sensor_id parameter error'
           print(error)
           return error, 500
        
        db = get_db()
        cursor = db.execute(f'''SELECT timestamp 
                               FROM {table_name}
                               WHERE sensor_id = {sensor_id}
                               ORDER BY timestamp 
                               DESC LIMIT 1''')
        
        rows = cursor.fetchall()
        last_timestamp = 0 if len(rows) == 0 else rows[0]['timestamp'] 
        return json.dumps({"last_timestamp" : last_timestamp}), 200

    except Exception as error:
        print(error)
        return str(error), 500
        
@bp.route('/temperatures_last/', methods=['GET'])
def get_temperatures_last():
    return get_last(request, 0)
    
@bp.route('/airflows_last/', methods=['GET'])
def last():
    return get_last(request, 1)

def get_last(request:Request, type:int):
    try:
        sensor_id = get_sensor_id(request)
        if sensor_id == 0:
           error = 'sensor_id parameter error'
           print(error)
           return error, 500
        
        db = get_db()
        sql = ""
        if(type == 0): 
            sql = get_airflows_last_sql(sensor_id)
        if(type == 1): 
            sql = get_temperatures_last_sql(sensor_id)   
        cursor = db.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            return 'There is no data', 500    
        
        return json.dumps(rows[0]), 200

    except Exception as error:
        print(error)
        return str(error), 500    

def get_airflows_last_sql(sensor_id:int):
    return f'''SELECT sensor_id,
                      timestamp, 
                      air_flow_rate,
                      temperature, 
                      air_consumption, 
                      DATETIME(timestamp, 'unixepoch', 'localtime') as datetime 
                FROM airflows 
                WHERE sensor_id = {sensor_id}
                ORDER BY timestamp DESC 
                LIMIT 1'''

def get_temperatures_last_sql(sensor_id:int):
    return f'''SELECT sensor_id,
                      timestamp, 
                      temperature, 
                      humidity, 
                      DATETIME(timestamp, 'unixepoch', 'localtime') as datetime 
                FROM temperatures 
                WHERE sensor_id = {sensor_id}
                ORDER BY timestamp DESC 
                LIMIT 1'''

@bp.route('/connectivity/', methods=['GET'])
def connectivity():
   success = {'is_connected': 1}
   failure = {'is_connected': 0}
   try:
      if(ping('172.16.1.2')._responses[0].success):
        return json.dumps(success), 200  
      else:
        failure['error'] = 'ping failure'
        return json.dumps(failure), 200  
   except Exception as e: 
      failure['error'] = str(e)
      return json.dumps(failure), 200