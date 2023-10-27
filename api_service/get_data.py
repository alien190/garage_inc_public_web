from .measurments import measurments_from_json, measurments_from_rows
from flask import (Blueprint, json, request)
from .db import get_db
from pythonping import ping

bp = Blueprint('get_data', __name__, url_prefix='/get_data')

@bp.route('/measurings/', methods=['GET'])
def measurings():
    try:
        print(request.args)
        db = get_db()
        cursor = db.execute("SELECT * FROM measurings")
        rows = cursor.fetchall()
        measurments = measurments_from_rows(rows)
        return json.dumps(measurments.__dict__), 200

    except Exception as error:
        print(error)
        return str(error), 500
    
@bp.route('/last_timestamp/', methods=['GET'])
def last_timestamp():
    try:
        db = get_db()
        cursor = db.execute("SELECT timestamp FROM measurings ORDER BY timestamp DESC LIMIT 1")
        rows = cursor.fetchall()
        last_timestamp = 0 if len(rows) == 0 else rows[0]['timestamp'] 
        return json.dumps({"last_timestamp" : last_timestamp}), 200

    except Exception as error:
        print(error)
        return str(error), 500
    

@bp.route('/last/', methods=['GET'])
def last():
    try:
        db = get_db()
        cursor = db.execute("SELECT timestamp, temperature, humidity, DATETIME(timestamp, 'unixepoch', 'localtime') as datetime FROM measurings ORDER BY timestamp DESC LIMIT 1")
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