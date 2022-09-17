import pickle
import numpy as np 
import pandas as pd 
import datetime

# from NewYork_Location import Location_list,coordinate_list
from NewYork_Location import *

path="xgb78.pkl"
model = pickle.load(open('xgb78.pkl', 'rb'))

input_cols = ['passenger_count',
       'trip_distance', 'year', 'month', 'day', 'weekday',
       'pickup_datetime_hour']

df_cols = ['pickup_datetime','pickup_longitude', 'pickup_latitude',
       'dropoff_longitude', 'dropoff_latitude', 'passenger_count']




#14 33 2014-01-23 ['Statue of Liberty'] ['Center Park'] 2 tuple
# %Y-%m-%d %H:%M:%S.%f'

def input_processing(input_data):
    pickup='new York'
    dropoff="new York"

    clock_hours,clock_min,book_date,pickup_point,dropoff_point,passenger_count=input_data

    #create picktime format
    date_format=f"{str(book_date)} {str(clock_hours)}:{str(clock_min)}:00"

    for x in pickup_point:
        pickup=x
    
    for y in dropoff_point:
        dropoff=y

    #find latitude and logitiude of pickup location
   
    location = coordinate_list.get(pickup,[-74.0099, 40.7126])
    print(pickup)
    #print(location.address)
    pickup_lati=location[1]
    pickup_logi=location[0]
    #print((location.latitude, location.longitude))

    #find latitude and logitiude of dropoff location
    
    #from geopy.geocoders import Nominatim 
    location = coordinate_list.get(dropoff,[-73.7781, 40.6413])
    print(dropoff)
    #print(location.address)
    dropoff_lati=location[1]
    dropoff_logi=location[0]
    inp_user=[[date_format,pickup_logi,pickup_lati,dropoff_logi,dropoff_lati,passenger_count]]
    print(inp_user)
    df = pd.DataFrame(inp_user,columns=df_cols)
    #print(date_format,pickup_lati,pickup_logi,dropoff_lati,dropoff_logi,passenger_count)
    df=add_trip_distance(df)

    df=add_dateparts(df,'pickup_datetime')

    df = df.drop('pickup_datetime', axis=1)
    #print("df shape : ",df.shape)

    #print("Input : \n",df)
    # output=model.predict(df)
    # print("\n >> Fare Amount : ",output)

    return df[input_cols]
#1
def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

#2
def add_trip_distance(df):
    df['trip_distance'] = haversine_np(df['pickup_longitude'], df['pickup_latitude'], df['dropoff_longitude'], df['dropoff_latitude'])
    return df

#3
def add_dateparts(df, col):
    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S.%f')
    df['year'] = df[col].dt.year
    df['month'] = df[col].dt.month
    df['day'] = df[col].dt.day
    df['weekday'] = df[col].dt.weekday
    df[col + '_hour'] = df[col].dt.hour
    df.drop(col,axis=1)
    return df

