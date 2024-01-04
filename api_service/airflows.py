from dacite import from_dict
from dataclasses import dataclass
from typing import List

@dataclass
class Airflow_model:
    timestamp:int
    sensor_id:int
    m5: int
    m15: int
    m30: int
    h1: int
    h4: int
    d1: int
    air_flow_rate: float
    temperature: float
    air_consumption: float

@dataclass
class Airflows_model:
    values: List[Airflow_model]

def airflows_from_json(json):
    return from_dict(data_class=Airflows_model, data=json)

def airflows_from_rows(rows):
    values = Airflows_model([])
    for row in rows:
      value = from_dict(data_class=Airflow_model, data=row) 
      values.values.append(value)

    return values