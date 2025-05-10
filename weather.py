import requests
from datetime import datetime
def Getpollution(lon,lat):
    API_Key ="65dab33592af356944a01e1f66db4a8f"
    url =f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=65dab33592af356944a01e1f66db4a8f"
    response = requests.get(url)
    return response

def GetWeather(city_name):
    API_Key ="65dab33592af356944a01e1f66db4a8f"
    # print(city_name)
    url =f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=65dab33592af356944a01e1f66db4a8f"
    response = requests.get(url)
    # print(response)
    return response

city_name=input("ENTER CITY NAME :")
response = GetWeather(city_name)
# print(response)
if response.status_code==200:
    api_data = response.json()
    # print(api_data)
    lon=api_data['coord']['lon']
    lat=api_data['coord']['lat']
    print(lon)
    print(lat)
    response2 = Getpollution(lon,lat)
    if response2.status_code==200:
        api_data2 = response2.json()
        print(api_data2)
        aqi=api_data2['list'][0]['main']['aqi']
        print("aqi         :",aqi)
        if(aqi==1):
         print("good")
        elif(aqi==2):
          print("fair")
        elif(aqi==3):
          print("moderate")
        elif(aqi==4):
          print("poor")
        elif(aqi==5):
          print("very poor")
    temp_city=((api_data['main']['temp'])-273.15)