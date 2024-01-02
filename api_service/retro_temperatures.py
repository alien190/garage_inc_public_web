from dacite import from_dict
from dataclasses import dataclass
from typing import List

@dataclass
class Retro_temperature_model:
    timestamp:int
    sensor_id:int
    temperature: float
    humidity:float

@dataclass
class Retro_temperatures_model:
    values: List[Retro_temperature_model]

def retro_temperatures_from_rows(rows):
    temperatures = Retro_temperatures_model([])
    for row in rows:
      temperature = from_dict(data_class=Retro_temperature_model, data=row) 
      temperatures.values.append(temperature)

    return temperatures

