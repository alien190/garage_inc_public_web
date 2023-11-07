from .measurments import measurments_from_rows
from .retro_measurment import retro_measurments_from_rows
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

@bp.route('/retro/', methods=['GET'])
def measurings():
    try:
        sensor_id = get_sensor_id(request)
        if sensor_id == 0:
           error = 'sensor_id parameter error'
           print(error)
           return error, 500
        
        db = get_db()
        period = request.args.get('period', 'm1')
        sql = get_measurings_sql(period)
        cursor = db.execute(sql)
        rows = cursor.fetchall()
        measurments = retro_measurments_from_rows(rows)
        return json.dumps(measurments.__dict__), 200

    except Exception as error:
        print(error)
        return str(error), 500

def get_measurings_sql(period:str, sensor_id:int):
    period = period.lower()
    
    if not period in allowed_periods:
        period = 'm1'
    
    if(period == 'm1'):
        return f'''SELECT timestamp,temperature,humidity,sensor_id 
                  FROM measurings 
                  WHERE sensor_id = {sensor_id}
                  ORDER BY timestamp DESC
                  LIMIT 100'''

    
    return f'''SELECT {period} as timestamp, 
                     avg(temperature) as temperature, 
                     avg(humidity) as humidity,
                     sensor_id
               FROM measurings 
               WHERE sensor_id = {sensor_id}
               GROUP BY {period}
               ORDER BY timestamp DESC
               LIMIT 100'''

@bp.route('/last_timestamp/', methods=['GET'])
def last_timestamp():
    try:
        sensor_id = get_sensor_id(request)
        if sensor_id == 0:
           error = 'sensor_id parameter error'
           print(error)
           return error, 500
        
        db = get_db()
        cursor = db.execute(f'''SELECT timestamp 
                               FROM measurings 
                               WHERE sensor_id = {sensor_id}
                               ORDER BY timestamp 
                               DESC LIMIT 1''')
        
        rows = cursor.fetchall()
        last_timestamp = 0 if len(rows) == 0 else rows[0]['timestamp'] 
        return json.dumps({"last_timestamp" : last_timestamp}), 200

    except Exception as error:
        print(error)
        return str(error), 500
    

@bp.route('/last/', methods=['GET'])
def last():
    try:
        sensor_id = get_sensor_id(request)
        if sensor_id == 0:
           error = 'sensor_id parameter error'
           print(error)
           return error, 500
        
        db = get_db()
        cursor = db.execute(f'''SELECT sensor_id,
                                       timestamp, 
                                       temperature, 
                                       humidity, 
                                       DATETIME(timestamp, 'unixepoch', 'localtime') as datetime 
                                FROM measurings 
                                WHERE sensor_id = {sensor_id}
                                ORDER BY timestamp DESC 
                                LIMIT 1''')
        rows = cursor.fetchall()
        if len(rows) == 0:
            return 'There is no data', 500    
        
        return json.dumps(rows[0]), 200

    except Exception as error:
        print(error)
        return str(error), 500    
    

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