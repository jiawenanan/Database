\connect x;

CREATE SCHEMA w;

--CREATE TYPE regiontype AS ENUM ('City', 'County', 'State', 'Country');
--CREATE TABLE statetable --completed
--(
--    statecodefips INT NOT NULL,
--    state_name VARCHAR(50),    
--    region_type regiontype,
--    PRIMARY KEY (statecodefips)
--);


CREATE TABLE w.county --completed
(
    county_id INT NOT NULL,
    county_name VARCHAR(50),
    metro VARCHAR(256),
    statecodefips INT, --NOT NULL REFERENCES statetable
    size_rank INT,
    municipalcodefips INT,
    PRIMARY KEY (county_id)
);

-- we also have two row of data, which is called Missing and Out Of State
--INSERT INTO county (county_id, county_name, statecodefips) VALUES ('0', 'Missing', '0');


CREATE TABLE w.address --completed
(
    address VARCHAR(255) NOT NULL,
    zip_code INT,    
    city VARCHAR(255),
    county_id INT NOT NULL REFERENCES county,
    PRIMARY KEY (address)
);

CREATE TABLE w.food --completed
(
   license_number INT NOT NULL,
   operation_type VARCHAR(255) DEFAULT 'Store',
   establishment_type VARCHAR(20),
   entity_name VARCHAR(255),
   dba_name VARCHAR(255),
   square_footage INT,
   latitude_longitude VARCHAR(255),
   address VARCHAR(255) NOT NULL REFERENCES address ON UPDATE CASCADE ON DELETE SET NULL,
   PRIMARY KEY (license_number)
);


CREATE TABLE w.vpf--completed
(
  county_id INT NOT NULL REFERENCES county,
  year_id INT NOT NULL,
  population INT,
  index_count INT,
  index_rate decimal(10, 1),
  violent_count INT,
  violent_rate decimal(10, 1),
  property_count INT,
  property_rate decimal(10, 1),
  firearm_count INT,
  firearm_rate decimal(10, 1),
  PRIMARY KEY (county_id, year_id)
 );

CREATE TYPE gender AS ENUM ('Male', 'Female','Missing');


CREATE TABLE w.prison --completed
(
  case_id INT NOT NULL,
  admission_year INT,
  admission_month INT,
  admission_type VARCHAR(255),
  county_id_commitment INT NOT NULL REFERENCES county,
  county_id_last_known_residence INT NOT NULL REFERENCES county,
  gender gender,
  age_at_admission INT,
  most_serious_crime VARCHAR(255),
  PRIMARY KEY (case_id),
  UNIQUE (case_id)
);

CREATE TABLE w.houseprice --completed
(
   county_id INT NOT NULL REFERENCES county,
   month_year DATE NOT NULL,
   price INT,
   PRIMARY KEY (county_id, month_year)
);


--we noticed that even the zipcode and city are the same, they may in different county
--in other word, zipcode cannot determine the city, zipcode + city cannot determine the 
--county(we did some research
--google gives the explanation as:Some cities cross into five different counties and as
--many as 20% of the ZIP Codes cross county lines)


-- only three row data in {state} table, because we only explore the New York State.
-- in order to maintain our database for future use, we added {state} table

COPY county
FROM '/Users/zhangxingpu/Desktop/countytable.csv' 
WITH (
  FORMAT CSV,
  HEADER true,
  NULL ''
);

COPY address
FROM '/Users/zhangxingpu/Desktop/addresstable.csv'
WITH (
  FORMAT CSV,
  HEADER true,
  NULL ''
);

COPY food
FROM '/Users/zhangxingpu/Desktop/foodtable.csv'
WITH (
  FORMAT CSV,
  HEADER true,
  NULL ''
);

COPY vpf
FROM '/Users/zhangxingpu/Desktop/vpftable.csv'
WITH (
  FORMAT CSV,
  HEADER true,
  NULL ''
);

COPY prison
FROM '/Users/zhangxingpu/Desktop/prisontable.csv'
WITH (
  FORMAT CSV,
  HEADER true,
  NULL ''
);

COPY houseprice
FROM '/Users/zhangxingpu/Desktop/housepricetable.csv'
WITH (
  FORMAT CSV,
  HEADER true,
  NULL ''
);



-- conda install --channel conda-forge geopandas
