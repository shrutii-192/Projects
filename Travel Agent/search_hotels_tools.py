import requests
from langchain.tools import tool
from dotenv import load_dotenv
from wether_tool import get_cordinates
import os
import json

# load env variables
load_dotenv()
GEOAPIFY = os.getenv("GEOAPIFY")
TRAVEL_AMADEUS_KEY = os.getenv("TRAVEL_AMADEUS_KEY")
TRAVEL_AMADEUS_SECRETE = os.getenv("TRAVEL_AMADEUS_SECRETE")
# MAKECORPS_Hotel_PRICE_API_KEY = os.getenv("MAKECORPS_Hotel_PRICE_API_KEY")
# OPENMAPTRIP_API_KEY = os.getenv("OPENMAPTRIP_API_KEY")





# def get_coordinates_geo(city):
#     coordinates = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={OPENMAPTRIP_API_KEY}"
#     response = requests.get(coordinates)
#     if response.status_code==200:
#         data = response.json()
#         lat = data['lat']
#         lon = data['lon']
#         return lat,lon
# x = get_coordinates_geo('pune')
# print(x)
# search attractive places  function
def get_search_attraction(latitude,longitude,city_name):
    places = f"https://api.opentripmap.com/0.1/en/places/radius?radius=5000&lon={longitude}&lat={latitude}&rate=2&format=json&apikey={OPENMAPTRIP_API_KEY}"
    response = requests.get(places)
    try:
        if response.status_code==200:
            data = response.json()
            lst1=[]
            for i in range(1,len(data)):
                rate = data[i]['rate']
                if rate == 7:
                    tagline = "🏛️ World-Famous Landmark"
                elif rate == 6:
                    tagline = "🌟 Must-See Attraction"
                elif rate >= 4:
                    tagline = "👍 Popular Spot"
                elif rate >= 2:
                    tagline = "🔍 Hidden Gem"
                else:
                    tagline = "🤓 Off the Beaten Path"
                dict={}
                dict['name'] = data[i]['name']
                dict['rate'] = data[i]['rate']
                dict['tagline'] = tagline
                lst1.append(dict)
            result = []
            for attr in lst1:
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

            return {"city": city_name, "highlights": result}
            
        else:
            print("Could not able to search the most attractive places")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# find country, countrycode , placeid, coordinates
def get_place_id(city_name):
    placeid = f"https://api.geoapify.com/v1/geocode/search?text={city_name}&apiKey={GEOAPIFY}"
    response = requests.get(placeid)
    try: 
        if response.status_code==200:
            data = response.json()
            country = data['features'][0]['properties']['country']
            country_code = data['features'][0]['properties']['country_code']
            placeid = data['features'][0]['properties']['place_id']
            coordinates = data['features'][0]['geometry']['coordinates']
            return country,country_code,placeid,coordinates
            
        else:
            return "Not able to invoke placeid or coordinates"
    except Exception as e:
        print(f"Error while invoking placeid or coordinates{e}")

#search restaurant function
def get_search_restaurant(place_id):
    restaurant = f"https://api.geoapify.com/v2/places?categories=catering.restaurant&filter=place:{place_id}&limit=20&apiKey={GEOAPIFY}"
    response = requests.get(restaurant)
    if response.status_code==200:
        data = response.json()
        restolst=[]
        for resto in data.get('features', []):
            props = resto.get('properties', {})
            raw = props.get('datasource', {}).get('raw', {})  # raw data might be nested
            geometry = resto.get('geometry', {})
            restaurant_info = {
            
                "restaurant_name": props.get('name', 'Unnamed'),
                "restaurant_address": props.get('formatted', 'N/A'),
                "email": raw.get('email', 'N/A'),
                "mobile": raw.get('phone', 'N/A'),  # Note: Geoapify may use 'phone'
                "website": raw.get('website', 'N/A'),
                "opening_hours": raw.get('opening_hours', 'N/A'),
                "facilities": props.get("facilities", {}),
                "diet": {
                    "vegetarian": props.get("catering", {}).get("diet", {}).get("vegetarian", False),
                    "non_vegetarian": props.get("catering", {}).get("diet", {}).get("non-vegetarian", False)
                },
                "place_id": props.get('place_id'),
                "coordinates": geometry.get('coordinates'),
                "catering_tags": props.get('catering', 'N/A')
            }
            restolst.append(restaurant_info)

        return restolst
    else:
        return {"error": f"Geoapify returned status code {response.status_code}"}

       
#search cafee function
def get_search_cafees(place_id):
    cafees_url = f"https://api.geoapify.com/v2/places?categories=catering.cafe&filter=place:{place_id}&limit=20&apiKey={GEOAPIFY}"
    response = requests.get(cafees_url)
    if response.status_code==200:
        data = response.json()
        cafe_list = []

        for cafe in data.get('features', []):
            props = cafe.get('properties', {})
            raw = props.get('datasource', {}).get('raw', {})
            geometry = cafe.get('geometry', {})

            cafe_info = {
                "name": props.get("name", "Unnamed"),
                "formatted": props.get("formatted", "N/A"),
                "country_code": props.get("country_code", "N/A"),
                "county": props.get("county", "N/A"),
                "website": props.get("website", raw.get("website", "N/A")),
                "catering": props.get("catering", {}),
                "place_id": props.get("place_id", "N/A"),
                "geometry": geometry.get("coordinates", []),
                "opening_hours": props.get("opening_hours", raw.get("opening_hours", "N/A")),
                "cuisine": props.get("catering", {}).get("cuisine", raw.get("cuisine", "N/A"))
            }
            cafe_list.append(cafe_info)
        return cafe_list
    else:
        return {"error": f"Geoapify request failed with status code {response.status_code}"}



def get_top_rated_hotels(place_id,lon,lat):
    hotels = f"https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=place:{place_id}&bias=proximity:{lon},{lat}&limit=20&apiKey={GEOAPIFY}"
    response = requests.get(hotels)
    if response.status_code==200:
        data = response.json()
        hotels = []
        for hotel in data.get('features', []):
            hoteldict = {}  # New dictionary per hotel
            properties = hotel.get('properties', {})
            geometry = hotel.get('geometry', {})
            hoteldict["hotel_name"] = properties.get('name', 'Unnamed')
            hoteldict["hotel_address"] = properties.get('formatted', 'N/A')
            hoteldict["distance"] = properties.get('distance')  # Distance may not be in 'properties'
            hoteldict["placeid"] = properties.get('place_id')
            hoteldict["coordinates"] = geometry.get('coordinates')
            hotels.append(hoteldict)
        return f"top rate hotels: {hotels}"
    
def get_search_activities(place_id):
    activity_url = f"https://api.geoapify.com/v2/places?categories=entertainment,leisure.park,sport&filter=place:{place_id}&limit=20&apiKey={GEOAPIFY}"
    response = requests.get(activity_url)
    if response.status_code==200:
        data = response.json()
        activities = []
        for activity in data.get("features", []):
            props = activity.get("properties", {})
            raw = props.get("datasource", {}).get("raw", {})
            geometry = activity.get("geometry", {})

            activity_info = {
                "name": props.get("name", "Unnamed"),
                "country_code": props.get("country_code", "N/A"),
                "state": props.get("state", "N/A"),
                "formatted": props.get("formatted", "N/A"),
                "categories": props.get("categories", []),
                "tourism": raw.get("tourism", "N/A"),
                "place_id": props.get("place_id", "N/A"),
                "geometry": geometry.get("coordinates", []),
                "distance": props.get("distance", "N/A")
            }
            activities.append(activity_info)
        return activities
    else:
        return {"error": f"Request failed with status code {response.status_code}"}


# for flight search

def get_amadeus_token(client_id, client_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=payload)
    return response.json().get("access_token")

# def get_city_activities(access_token, latitude, longitude):
#     url = "https://test.api.amadeus.com/v1/shopping/activities"
#     params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "radius": 1200,
#         "radiusUnit": "KM"
#     }
#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = requests.get(url, headers=headers, params=params)
#     print(response.status_code)
#     if response.status_code==200:
#         data =  response.json()

def get_location_code(access_token, keyword):
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    params = {
        "keyword": keyword,
        "subType": "CITY,AIRPORT",
        "page[limit]": 1
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()
import time
def get_search_flights(access_token, origin, destination, departure_date):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
        "nonStop": "false",
        "max": 5
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params=params)
    data =response.json()
    return data

def get_extract_flight_info(flight_data):
    simplified_flights = []
    for offer in flight_data.get("data", []):
        price = offer["price"]["grandTotal"]
        currency = offer["price"]["currency"]
        itinerary = offer["itineraries"][0]
        segments = []

        for seg in itinerary["segments"]:
            segments.append({
                "from": seg["departure"]["iataCode"],
                "to": seg["arrival"]["iataCode"],
                "departure_time": seg["departure"]["at"],
                "arrival_time": seg["arrival"]["at"],
                "carrier": seg["carrierCode"],
                "flight_number": seg["number"],
                "duration": seg["duration"],
                "stops": seg["numberOfStops"]
            })

        bags = offer["travelerPricings"][0]["fareDetailsBySegment"][0]
        simplified_flights.append({
            "price": f"{currency} {price}",
            "duration": itinerary["duration"],
            "segments": segments,
            "cabin": bags.get("cabin", "N/A"),
            "baggage": {
                "checked": f"{bags['includedCheckedBags']['weight']} {bags['includedCheckedBags']['weightUnit']}",
                "cabin": f"{bags['includedCabinBags']['weight']} {bags['includedCabinBags']['weightUnit']}"
            },
            "refundable": any(a["description"] == "REFUNDABLE TICKET" and not a["isChargeable"]
                              for a in bags.get("amenities", [])),
            "changeable": any(a["description"] == "CHANGEABLE TICKET" and not a["isChargeable"]
                              for a in bags.get("amenities", []))
        })

    return simplified_flights



# find the price of hotel ut don't have access to test 
# def search_hotels_by_city(access_token, city_code):
#     url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
#     params = {"cityCode": city_code}
#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = requests.get(url, headers=headers, params=params)
#     return response.json().get("data", [])

# def get_hotel_price_by_id(access_token, hotel_id):
#     url = "https://test.api.amadeus.com/v3/shopping/hotel-offers/by-hotel"
#     headers = {"Authorization": f"Bearer {access_token}"}
#     params = {"hotelId": hotel_id}
#     response = requests.get(url, headers=headers, params=params)
#     data = response.json()
#     return data

# def extract_hotel_ids(hotel_list):
#     return [hotel.get("hotelId") for hotel in hotel_list if "hotelId" in hotel]

# def get_all_hotel_prices(access_token, hotel_ids):
#     results = []
#     for hotel_id in hotel_ids:
#         try:
#             # time.sleep(delay)  # Prevent API rate-limiting
#             response = get_hotel_price_by_id(access_token, hotel_id)
#             print(response)
#             offers = response.get("data", {}).get("offers", [])
#             if offers:
#                 price = offers[0].get("price", {}).get("total")
#                 name = response.get("data", {}).get("hotel", {}).get("name", "Unknown Hotel")
#                 results.append({
#                     "hotelId": hotel_id,
#                     "name": name,
#                     "price_eur": price
#                 })
#         except Exception as e:
#             print(f"Error fetching hotel {hotel_id}: {e}")
#     return results

# def tag_hotel_budget(eur_price):
#     try:
#         inr = float(eur_price) * 90  # Rough conversion, feel free to update
#         if inr < 3000:
#             return "🟢 Budget"
#         elif inr < 7000:
#             return "🟡 Mid-range"
#         else:
#             return "🔴 Luxury"
#     except:
#         return "⚪ Unknown"
# def get_multiple_hotel_prices(access_token, hotel_ids):
#     results = []
#     for hotel_id in hotel_ids:
#         if not isinstance(hotel_id, str) or not hotel_id.strip():
#             print(f"Skipping invalid hotel ID: {hotel_id}")
#             continue
#         try:
#             time.sleep(2)  # Avoid hitting rate limits
#             data = get_hotel_price_by_id(access_token, hotel_id)
#             print(data)
#             price = data.get("data", {}).get("offers", [{}])[0].get("price", {}).get("total")
#             name = data.get("data", {}).get("hotel", {}).get("name", "Unknown")
#             if price:
#                 results.append({"id": hotel_id, "name": name, "price_eur": price})
#         except Exception as e:
#             print(f"Error fetching {hotel_id}: {e}")
#     return results

# x = get_amadeus_token(TRAVEL_AMADEUS_KEY,TRAVEL_AMADEUS_SECRETE)
# # y = get_cordinates('Mumbai')
# y = get_location_code(x,'Mumbai')
# # print(y['data'][0]['iataCode'])
# time.sleep(1)
# z =search_hotels_by_city(x,y['data'][0]['iataCode'])
# # print(z)
# time.sleep(1)
# id = extract_hotel_ids(z)[:1]
# print(id)
# time.sleep(1)
# m = get_hotel_price_by_id(x,id)
# print(m)
# hotel_prices = get_multiple_hotel_prices(x, 'HOBOM009')
# print(hotel_prices)

# for hotel in hotel_prices:
#     print(f"{hotel['name']} – Hotel ID: {hotel['hotelId']} – €{hotel['price_eur']}")



"""
Go inside tool for flight offers
x = get_amadeus_token(TRAVEL_AMADEUS_KEY,TRAVEL_AMADEUS_SECRETE)
y = get_location_code(x,'Mumbai')
# print(y['data'][0]['iataCode'])
time.sleep(1)
w= get_location_code(x,'Pune')
# print(w['data'][0]['iataCode'])
time.sleep(1)
z =search_flights(x,y['data'][0]['iataCode'],w['data'][0]['iataCode'],"2025-06-25")
# cls
time.sleep(1)
t = extract_flight_info(z)
print(t)



# x = get_place_id('pune')
# print(x[2],x[3][0],x[3][1])
# # y = get_top_rated_hotels(x[2],x[3][0],x[3][1])
# # print(y)
# y=get_search_activities(x[2])
# print(y)

# x = get_cordinates('Pune')
# print(x)
# y = get_cordinates('mumbai')
# print(y)
# z = get_search_local_transport(x,y)

# print(z)
"""


