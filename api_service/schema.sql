DROP TABLE IF EXISTS airflows;
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

CREATE TABLE airflows ( 
    timestamp INT NOT NULL, 
    sensor_id INT NOT NULL, 
    m5 INT NOT NULL, 
    m15 INT NOT NULL, 
    m30 INT NOT NULL, 
    h1 INT NOT NULL, 
    h4 INT NOT NULL, 
    d1 INT NOT NULL, 
    air_flow_rate FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    air_consumption FLOAT NOT NULL,
    PRIMARY KEY (timestamp, sensor_id)
);