DROP TABLE IF EXISTS measurings;
DROP TABLE IF EXISTS temperatures;

CREATE TABLE temperatures ( 
    timestamp INT NOT NULL, 
    sensor_id INT NOT NULL, 
    m5 INT NOT NULL, 
    m15 INT NOT NULL, 
    m30 INT NOT NULL, 
    h1 INT NOT NULL, 
    h4 INT NOT NULL, 
    d1 INT NOT NULL, 
    temperature FLOAT NOT NULL,  
    humidity FLOAT NOT NULL,
    PRIMARY KEY (timestamp, sensor_id)
);