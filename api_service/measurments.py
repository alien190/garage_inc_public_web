from dacite import from_dict
from dataclasses import dataclass
from typing import List

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

def measurments_from_json(json):
    return from_dict(data_class=Measurments_model, data=json)

def measurments_from_rows(rows):
    measurments = Measurments_model([])
    for row in rows:
      measurment = from_dict(data_class=Measurment_model, data=row) 
      measurments.measurments.append(measurment)

    return measurments

