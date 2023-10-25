from api_service.measurments import measurments_from_json, measurments_from_rows
from flask import (Blueprint, json, request)
from api_service.db import get_db

bp = Blueprint('get_data', __name__, url_prefix='/get_data')

@bp.route('/', methods=['GET'])
def register():
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