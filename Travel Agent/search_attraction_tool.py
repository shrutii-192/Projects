import requests
from langchain.tools import tool
from dotenv import load_dotenv
from wether_tool import get_cordinates
from search_hotels_tools import get_place_id,get_search_activities,get_search_restaurant,get_search_cafees,get_top_rated_hotels,get_search_attraction,get_amadeus_token,get_location_code,get_search_flights,get_extract_flight_info
import os
import json
import time

load_dotenv()
OPENMAPTRIP_API_KEY = os.getenv("OPENMAPTRIP_API_KEY")
TRAVEL_AMADEUS_KEY = os.getenv("TRAVEL_AMADEUS_KEY")
TRAVEL_AMADEUS_SECRETE = os.getenv("TRAVEL_AMADEUS_SECRETE")
# This tool search the attractive places 
@tool
def search_attraction_tool(city_name:str)->dict:
    """
    Search the attractions and point of interest around the world. It searches the attractive places 
    within 5km circle of particular city or place and rate the popular places in a range of 1-7, with higher
    numbers indicating a more well known or frequently visited attraction.
    Args: 
        city_name(str): withing 5Km circles tool will sarch the more attractive and frequently visited places.
    Returns: 
        list: list of dictionaries which inclueds all attractive places along with the ratings of each and every place 
    """
    try:
        if city_name is not None:
            lat,long = get_cordinates(city_name)
            # lat,long = get_coordinates(city_name)
            attractions = get_search_attraction(lat,long)
            result = []
            for attr in attractions:
                name = attr.get("name", "Unknown")
                rate = attr.get("rate", 0)
                tagline = (
                    "🏛️ World-Famous Landmark" if rate == 7 else
                    "🌟 Must-See Attraction" if rate == 6 else
                    "👍 Popular Spot" if rate >= 4 else
                    "🔍 Hidden Gem" if rate >= 2 else
                    "🤓 Off the Beaten Path"
                )
                result.append(f"{tagline}: {name} (Rating: {rate})")

            return {"City_name": city_name, "Highlights": result}

            # return f"The attractive places near {city_name} will be {attractions}"
    except Exception as e:
        print("error while searching the attractions through tool")
        return {"error": str(e)}
    

@tool
def search_restaurant_tool(city_name:str)->dict:
    """
    Search the top rated restaurant according to city or country 
    Args: 
        city_name(str): sarch the top rated restaurants (eg. city, country)
    Returns: 
        list: list of dictionaries which inclueds all the information related to top rated restaurant, includes keys such as name of restaurnat, cuisins, address
        of restaurant, opening and closing hours diet each restaurant serve(eg. vegeterian, non-vegiterian).
    """
    try:
        if city_name is not None:
            country,country_code,placeid,coordinates = get_place_id(city_name)
            restaurant = get_search_restaurant(placeid)
            return {"City_name":city_name,"Resaurant_details":restaurant}
    except Exception as e:
        print("error while searching the top rated restaurant tool")
        return {"error": str(e)}
    

  

@tool
def search_cafees_tool(city_name:str)->dict:
    """
        Search the top rated cafees according to city or country 
        Args: 
            city_name(str): sarch the top rated cafees (eg. city, country)
        Returns: 
            list: list of dictionaries which inclueds all the information related to top rated cafees, includes keys such as name of cafees, cuisins, address
            of cafee,country,country_code, opening and closing hours,website.
    """
    try:
        if city_name is not None:
            country,country_code,placeid,coordinates = get_place_id(city_name)
            cafees = get_search_cafees(placeid)
            return {"City_name":city_name,"Cafee_details":cafees}
    except Exception as e:
        print("error while searching the top rated cafees tool")
        return {"error": str(e)}
        

@tool
def search_Activities_tool(city_name:str)->dict:
    """
        Search the activities which is categories as entertaintment, musem, theme parks, sports etc in 
        accordance with city or country name.  
        Args: 
            city_name(str): sarch the top rated restaurants (eg. city, country)
        Returns: 
            list: list of dictionaries which inclueds all the information related to activities user wants to perform, includes keys such as name of activity,
            category of activity,distance of the activity area from your city location
    """
    try:
        if city_name is not None:
            country,country_code,placeid,coordinates = get_place_id(city_name)
            activity = get_search_activities(placeid)
            return {"City_name":city_name,"Activity_details":activity}
    except Exception as e:
        print("error while searching the top rated cafees tool")
        return {"error": str(e)}

@tool 
def search_transportation_tool(city_name:str,departure_data:str)->dict:
    """
        Search the flight from oroginal location to destination location based on city code for particular data. format of data should be 
        ex('YYYY-MM-DD')
        accordance with city or country name.  
        Args: 
            city_name(str): sarch the top rated restaurants (eg. city, country)
        Returns: 
            list: list of dictionaries which inclueds all the fight information for te destination placce 
    """
    try:
        if city_name is not None:
            access_token = get_amadeus_token(TRAVEL_AMADEUS_KEY,TRAVEL_AMADEUS_SECRETE)
            original_location_code = get_location_code(access_token,city_name)
            time.sleep(1)
            destination_location_code= get_location_code(access_token,city_name)
            time.sleep(1)
            search_flights =get_search_flights(access_token,original_location_code['data'][0]['iataCode'],destination_location_code['data'][0]['iataCode'],departure_data)
            time.sleep(1)
            extract_flights_data = get_extract_flight_info(search_flights)
            return  extract_flights_data
    except Exception as e:
        print("error while searching the top rated cafees tool")
        return {"error": str(e)}










    