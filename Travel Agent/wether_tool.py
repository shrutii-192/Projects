import requests
from langchain.tools import tool


# extract coordinates of city
def get_cordinates(city_name):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1" # we can use this API as well for coordinates identfication f"https://api.opentripmap.com/0.1/en/places/geoname?name={city_name}&apikey={OPENMAPTRIP_API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            latitude = data['results'][0]['latitude']
            longitude = data['results'][0]['longitude']
            # print("-> Coordinates found <-")
            # print(f"Coordinates for {city_name}: Latitude: {latitude}, Longitude: {longitude}")
            return latitude, longitude
    

#extract current temperature and wether condition using coordinates
def get_temperature(latitude,longitude):
    weather_map = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
        55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        80: "Rain showers", 95: "Thunderstorm", 99: "Thunderstorm with hail"
    }

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        if data.get('current_weather'):
            temperature = data['current_weather']['temperature']
            weather_code_response = data['current_weather']['weathercode']
            weather_code = weather_map.get(weather_code_response, "Unknown weather code")
            # print("-> Weather data found <-")
            # print(f"Temperature: {temperature}°C, Weather Condition: {weather_code}")
            return temperature, weather_code
   

#weather tool
@tool
def Weathertool(city_name:str)->str:
    """ Extract the current temeperature and wether condition on the basis of city name
        Args: 
        city_name(str)- on the basis of city extract the current temperature and wether condition (eg. 'Pune', 'NewYork', 'US', 'London')
        Returns: 
        str:A message with the current wether condition.
    """
    try: 
        if city_name is not None:
            location = get_cordinates(city_name)
            temperature,weather_code = get_temperature(location[0],location[1])
            return f"Weather condition in {city_name} is {weather_code} and temperature is {temperature}"
        else:
            return f"city name is not provided"
    except Exception as e:
        return f"An error occurred while fetching temperature and weather condition: {str(e)}"




