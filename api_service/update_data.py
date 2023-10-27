from .measurments import measurments_from_json
from flask import (Blueprint, request)
from .db import get_db

bp = Blueprint('update_data', __name__, url_prefix='/update_data')

@bp.route('/', methods=['POST'])
def register():
    try:
        db = get_db()
        json = request.json
        measurments = measurments_from_json(json)
        
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
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                        ON CONFLICT(timestamp) DO UPDATE SET temperature = ?, humidity = ?"""
                
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
                
                db.execute(sql, val)

        db.commit()
        return 'Data was updated', 200

    except Exception as error:
        print(error)
        return str(error), 500