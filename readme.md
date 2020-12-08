Here are some instructions for this application.
This is a database query application which allowed the user to have a sense of living(house price and retail food) and safety(crime) condition in different county of New York State.

First Step:
(Please run retreive_data.py to download our original data.)
Notice！One of the original url will download a .zip file, our python code in step two will do unzip.

-----------------------------------------

Second Step:
(Please run schema.sql to create the schema)
Some explanation for our schema which may arouse your confusion:
1 For food datasets, why drop

-----------------------------------------

Third Step:
(Please run data_pre_norm.py to do data cleaning and database normalization)
Since the source of our four databases are different, the formats of data are also different, which requires a lot of data cleaning work without the data loss.
Also, in order to avoid data redundancy, we need normalization which requires more data preprocessing work. 

-----------------------------------------

Fourth Step:
(Please run data_load.py to load the preprocessed data into the database.)

-----------------------------------------

some explanation for schema:
in order to eleminate the data redundancy, we decide to extract latitude and longitude, all other data can be found in other columns
esult of data manipulation: 1558 unique zip_code, 
1452 unique city, 
1605 unique zipcode + county_id, 
1797 unique zipcode + city, 
1499 unique city + county_id
after data manipulation, we noticed that even ['zipcode'] + ['city'] cannot determine the ['county'] for our food dataset
the explanation we fetch from the google: google gives the explanation as:Some cities cross into five different counties and as many as 20% of the ZIP Codes cross county lines)



Five Step:
(Now, you can explore our database by the API we provide to you)
1
2
3
4
5
6