import requests
import pandas as pd
import pickle


def wind_data():
    APIKey = '1227d4783d99527fb95fbc6207c350e7'
    lat = 8.598084
    lon = 53.556563
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=hourly,current,minutely&appid={APIKey}"
    data = requests.get(url).json()
    #return data
    wind_speed =[]
    wind_direction =[]
    date =[]
    ct = 0
    for i in range (0,7):
        w_speed = data['daily'][ct]['wind_speed']
        wind_deg = data['daily'][ct]['wind_deg']
        dt = data['daily'][ct]["dt"]
        wind_speed.append(w_speed)
        wind_direction.append(wind_deg)
        date.append(dt)
        ct = ct + 1
    return [wind_speed, wind_direction, date]

def wind_dataframe():
    items = wind_data()
    column_names = ['wind speed', 'direction', 'Date']
    df = pd.DataFrame(items).transpose()
    df.columns = column_names
    df['Date'] = pd.to_datetime(df['Date'], unit = 's')
    df.set_index('Date', inplace = True)
    loaded_model = pickle.load(open("wind_model.pkl", 'rb'))
    predictions = loaded_model.predict(df.values)
    df['Power_Output_Predictions'] = predictions
    df['Date Of Month'] = df.index.day
    return df


def solar_data():
    url = 'http://www.7timer.info/bin/api.pl?lon=142.11.17&lat=-19.46&product=civil&output=json'
    url_2 = 'http://www.7timer.info/bin/api.pl?lon=142.11.17&lat=-19.46&product=civillight&output=json'
    data = requests.get(url).json() #Data for Weather Data
    data_2 = requests.get(url_2).json() #Data for Dates
    temp_hi = []
    temp_lo = []
    cloudcover =[]
    date = []
    j = 0
    for i in range (0,7):
        ccover = data['dataseries'][j]["cloudcover"]
        cloudcover.append(ccover)
        j = j + 7
    ct = 0
    for items in (data_2['dataseries']):
        dt = data_2['dataseries'][ct]['date']
        tm_hi = data_2['dataseries'][ct]['temp2m']['max']
        tm_lo = data_2['dataseries'][ct]['temp2m']['min']
        temp_hi.append(tm_hi)
        temp_lo.append(tm_lo)
        date.append(dt)
        ct = ct + 1
    return [temp_hi, temp_lo, cloudcover, date]

def solar_dataframe():
    items = solar_data()
    column_names = ['Temp Hi','Temp Low','Cloud Cover Percentage','Date']
    df = pd.DataFrame(items).transpose()
    df.columns = column_names
    df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y%m%d')
    df.set_index('Date', inplace = True)
    loaded_model = pickle.load(open("solar_model.pkl", 'rb'))
    predictions = loaded_model.predict(df.values)
    df['Power_Output_Predictions'] = predictions
    df['Date Of Month'] = df.index.day
    return df
