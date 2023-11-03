from dacite import from_dict
from dataclasses import dataclass
from typing import List

@dataclass
class Retro_measurment_model:
    timestamp:int
    sensor_id:int
    temperature: float
    humidity:float

@dataclass
class Retro_measurments_model:
    measurments: List[Retro_measurment_model]

def retro_measurments_from_rows(rows):
    measurments = Retro_measurments_model([])
    for row in rows:
      measurment = from_dict(data_class=Retro_measurment_model, data=row) 
      measurments.measurments.append(measurment)

    return measurments

