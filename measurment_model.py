from dataclasses import dataclass

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