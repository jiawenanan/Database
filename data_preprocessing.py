#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
import numpy as np
import zipfile
prison = pd.read_csv('~/Desktop/Prison_Admissions__Beginning_2008.csv')
house = pd.read_csv('~/Desktop/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv')
vpf = pd.read_csv('~/Desktop/Index__Violent__Property__and_Firearm_Rates_By_County__Beginning_1990.csv')
food =  pd.read_csv('~/Desktop/Retail_Food_Stores.csv')
##house = house.rename(columns={"RegionID": "county_id", "SizeRank": "size_rank","RegionName": "county_name","RegionType": "region_type","": "county_name"})
import re

## function for extract the first word
def first_word(text: str) -> str:
    return re.search("([\w']+)", text).group(1)

#---------------------------<houseprice>-------------------------------
##extract data for {houseprice} table

##transfer the time series as the value of column ['month_year']

old = ' County' ## we don't want "County" to be apeared in our ['county_name'] column
house = house[house['State'] == 'NY'] 
house['RegionName'] = house['RegionName'].apply(lambda x : x.replace(old, ''))
house.sort_values(by = 'SizeRank',axis = 0, ascending= True)
house.reset_index(drop=True, inplace=True)
time_index = house.columns[9:,]
column_countyid = []
column_time = []
column_price = []
for x in range(0,62):
    for y in range(0, 298):
        column_countyid.append(house.iloc[x,0])
        column_time.append(time_index[y])
        column_price.append(house.iloc[x,9 + y])
temp = pd.DataFrame()
temp['county_id'] = column_countyid
temp['month_year'] = column_time
temp['price'] = column_price
temp['price'] = temp['price'].astype(int)
## temp is the data for table {houseprice} (18476 * 3)
houseprice = temp
houseprice.to_csv('~/Desktop/housepricetable.csv', index = False)

#---------------------------<county>-------------------------------
##extract data for {county} table
temp1 = pd.DataFrame()
temp1['county_id'] = house['RegionID']
temp1['county_name'] = house['RegionName']
temp1['metro'] = house['Metro']
temp1['statecodefips'] = house['StateCodeFIPS']
temp1['size_rank'] = house.index + 1
temp1['municipalcodefips'] = house['MunicipalCodeFIPS']
## we change all NaN value to 'Missing' according to our plan,county is the fk, cannot be null
temp1['metro'] = temp1['metro'].fillna('Missing')
temp1 = temp1.append([{'county_id':0,'county_name':'Missing','metro':'Missing','statecodefips':0,'size_rank': 0,'municipalcodefips':0}], ignore_index=True)
county = temp1
county.to_csv('~/Desktop/countytable.csv', index = False)
## the preprocessed dataset includes 62 rows, however, in the final dataset there will be 63 rows,
## the 63rd row is ['Missing']
## for further expanding, we store the U.S-wide statecodefips in a mongodb database
## this application is focusing on New York State

## for further mapping use, make a county --> county_id dictionary
county_id = county.county_id.tolist()
county_name = county.county_name.tolist()
county_id_name = {}
for name in county_name:
    for i_d in county_id:
        county_id_name[name] = i_d
        county_id.remove(i_d)
        break
        
#---------------------------<vpf>-------------------------------
## extract data for {vpf} table
## map county to county_id, before doing that, we noticed that in table {county} --> 'Saint Lawrence', however, in original vpf table, it is 'St Lawrence' or 'St. Lawrence'
## so we need to change all 'St Lawrence' || 'St. Lawrence' in vpf table to be Saint Lawrance
vpf['County'].loc[(vpf['County'] == 'St Lawrence')] = 'Saint Lawrence'
vpf['County'].loc[(vpf['County'] == 'St. Lawrence')] = 'Saint Lawrence'
## Map to county_id(the primary key in {county} table)
vpf['County'] = vpf['County'].map(county_id_name) 
vpf = vpf.rename(columns={"County": "county_id", "Year":"year_id", "Population": "population", "Index Count" : "index_count", "Index Rate":"index_rate", "Violent Count" :"violent_count", "Violent Rate" :"violent_rate","Property Count":"property_count","Property Rate":"property_rate","Firearm Count":"firearm_count","Firearm Rate":"firearm_rate"})
vpf['population'] = vpf['population'].astype(int)
vpf['firearm_count'] = vpf['firearm_count'].astype(pd.Int32Dtype())
vpf.to_csv('~/Desktop/vpftable.csv', index = False)

#---------------------------<prison>-------------------------------
## extract data for {prison} table
## ['Admission Month'] and ['Month Code'] represent the same meaning without any explantion to users
## As there will be no data loss, we plan to drop ['Admission Month']
## 1) ['County of Commitment'] in prison dataset are all capitalized, we transfer it to be consistent with the table {county}
## we can sure that there will be no data missing for doing above-mentioned transformation
columns = prison.columns.tolist()
string_columns = [1,3,4,5,6,8]
for x in string_columns:
    prison[columns[x]] = prison[columns[x]].str.title() 
## we change all NaN value in ['County of Commitment'] column to 'Missing' according to our plan, county is the fk, cannot be null
prison['County of Commitment'] = prison['County of Commitment'].fillna('Missing')
prison = prison.drop(columns = ['Admission Month'])
## Assign case_id to each case as the pk
#prison['case_id'] = prison.index + 1
## change all 'St Lawrence' in prison table to be Saint Lawrance
prison['County of Commitment'].loc[(prison['County of Commitment'] == 'St Lawrence')] = 'Saint Lawrence'
prison['County of Commitment'].loc[(prison['County of Commitment'] == 'Brooklyn')] = 'New York'
prison['County of Commitment'].loc[(prison['County of Commitment'] == 'Manhattan')] = 'New York'
prison['County of Commitment'].loc[(prison['County of Commitment'] == 'Staten Island')] = 'New York'
prison['Last Known Residence County'] = prison['Last Known Residence County'].fillna('Missing')
prison['Last Known Residence County'].loc[(prison['Last Known Residence County'] == 'Richmond (Staten Island)')] = 'New York'
prison['Last Known Residence County'].loc[(prison['Last Known Residence County'] == 'New York (Manhattan)')] = 'New York'
prison['Last Known Residence County'].loc[(prison['Last Known Residence County'] == 'Kings (Brooklyn)')] = 'New York'
prison['Last Known Residence County'].loc[(prison['Last Known Residence County'] == 'Unknown')] = 'Missing'
prison['Last Known Residence County'].loc[(prison['Last Known Residence County'] == 'St Lawrence')] = 'Saint Lawrence'
prison['Last Known Residence County'].loc[(prison['Last Known Residence County'] == 'Out Of State')] = 'Missing'
## the data in column['Last Known Residence County'] is sort of different when compared with 62 county name in new york state
## for example: Kings (Brooklyn), New York (Manhattan), Rensselaer, Seneca, Westchester
## one county mapped with multiple ast Known Residence County, this column seems more like city.
## we decide to extract words in bracket, create a list to store all unique value and compare it with city in table{food}
#prison['Last Known Residence County'].apply(lambda x : y = re.findall('\((.*?)\)', x), unique_last_known_resi.append(y))
before_extract = prison['Last Known Residence County'].unique()
## create a new dataframe and drop the duplication to check the relationship between ['county'] & ['Last Known Residence County']
## the result is that, staten island, manhattan, and brooklyn, three city in newyork are only three value different from the county
## since both two columns talk about county, we eventually set above-mentioned value to be 'New York'
## as the same, do mapping to only reserve the county_id as fk
prison['County of Commitment'] = prison['County of Commitment'].map(county_id_name) 
prison['Last Known Residence County'] = prison['Last Known Residence County'].map(county_id_name) 
prison = prison.rename(columns={"Admission Year": "admission_year", "Month Code":"admission_month", "Admission Type": "admission_type", "County of Commitment" : "county_id_commitment", "Last Known Residence County":"county_id_last_known_residence", "Gender" :"gender", "Age at Admission" :" age_at_admission","Most Serious Crime":"most_serious_crime"})
prison.insert(0,'case_id',prison.index + 1) 
prison['gender'].loc[(prison['gender'].isnull())] = 'Missing'
prison['gender'].loc[(prison['gender'] == 'Not Coded')] = 'Missing'
#len(prison['County of Commitment'].unique())
#prison['county_id_last_known_residence'] 
prison.to_csv('~/Desktop/prisontable.csv', index = False)

#---------------------------<food>-------------------------------
food['City'] = food['City'].str.title() 
food['County'].loc[(food['County'] == 'St. Lawrence')] = 'Saint Lawrence'
## ['Location'] = ['Street Number'] + ['Street Name'] + ['latitude'] + ['longitude'] +['city'] +['Zip Code']
## in order to eleminate the data redundancy, we decide to extract latitude and longitude, all other data can be found in other columns
## result of data manipulation: 1558 unique zip_code, 1452 unique city, 1605 unique zipcode + county_id, 1797 unique zipcode + city, 1499 unique city + county_id
## after data manipulation, we noticed that even ['zipcode'] + ['city'] cannot determine the ['county'] for our food dataset
## the explanation we fetch from the google: google gives the explanation as:Some cities cross into five different counties and as many as 20% of the ZIP Codes cross county lines)
Location = []
for x in range(0, len(food)):
    if food.iloc[x]['Street Number'] != None:
        y = str(food.iloc[x]['Street Number']).strip()
        z = food.iloc[x]['Street Name'].strip()
        Location.append(y + ' ' + z)
    else:
        z = food.iloc[x]['Street Name'].strip()
        Location.append(z)
temp2 = pd.DataFrame()
temp2['address'] = Location 
temp2['zip_code'] = food['Zip Code']
temp2['city'] = food['City']
temp2['county_id'] = food['County'].map(county_id_name)
temp2 = temp2.drop_duplicates(['address'])
## Extract ['address'] for {address} table and {food} without data loss

#---------------------------<address>-------------------------------
temp2.to_csv('~/Desktop/addresstable.csv', index = False)
## data in address is not unique, duplication exist. For example: a Starbucks in a Walmart shares the same address with the Walmart 
## drop above-mentioned columns without any data loss
food = food.drop(columns = ['County','Street Number', 'Street Name','Address Line 2','Address Line 3','City','State','Zip Code'])
pair= []
def subString(location_column):
    for x in range(0, len(location_column)):
        if isinstance(location_column[x], str): 
            y = re.findall(r'[(](.*?)[)]',location_column[x])
            if len(y) != 0:
                pair.append(y[0])
            else:
                pair.append(None)
        else:
            pair.append(None)
## extract the latitude and longitude from food['Location']
subString(food['Location'])
food['latitude_longitude'] = pair
## drop ['Location'] and there is no data loss
food = food.drop(columns = ['Location'])
## add our processed location data to food
food['address'] = Location
food = food.rename(columns={"License Number": "license_number", "Operation Type":"operation_type", "Establishment Type": "establishment_type", "Entity Name" : "entity_name", "DBA Name":"dba_name", "Square Footage" :"square_footage"})
food.to_csv('~/Desktop/foodtable.csv', index = False)

## after the data preprocessing, you should have six .csv files on your desktop


# In[ ]:




