from dacite import from_dict
from dataclasses import dataclass
from typing import List

@dataclass
class Retro_airflow_model:
    timestamp:int
    sensor_id:int
    air_flow_rate: float
    temperature: float
    air_consumption: float

@dataclass
class Retro_airflows_model:
    values: List[Retro_airflow_model]

def retro_airflows_from_rows(rows):
    values = Retro_airflows_model([])
    for row in rows:
      value = from_dict(data_class=Retro_airflow_model, data=row) 
      values.values.append(value)

    return values

