from dacite import from_dict
from dataclasses import dataclass
from typing import List

@dataclass
class Temperature_model:
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
class Temperatures_model:
    values: List[Temperature_model]

def temperatures_from_json(json):
    return from_dict(data_class=Temperatures_model, data=json)

def temperatures_from_rows(rows):
    temperatures = Temperatures_model([])
    for row in rows:
      temperature = from_dict(data_class=Temperature_model, data=row) 
      temperatures.values.append(temperature)

    return temperatures