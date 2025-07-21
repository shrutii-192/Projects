import requests
from search_hotels_tools import get_place_id
from langchain.tools import tool
import os

GEOAPIFY = os.getenv("GEOAPIFY")


@tool
def currancy_conversion_tool(city_name_1:str,city_name_2:str,amount:int)->dict:
    """
    Converts currency from one city to another using live exchange rates.
    Args:
        amount(int)-amount to convert into new currancy
        from_currency(str)-from which currancy tool has to update the amount 
        to_currency(str)-to which currancy user has to update the amount
    Return:
        dict: contains information of amount exchange rate along with currancy converted amount
    """
    try:
        # Get currency codes for both cities
        _, code1, _, _ = get_place_id(city_name_1)
        _, code2, _, _ = get_place_id(city_name_2)
        currency_1 = get_currency_from_country_code(code1)
        currency_2 = get_currency_from_country_code(code2)
        conversion_result = get_convert_currancy(amount, currency_1, currency_2)
        return f"""currancy conversion and exchange rate will be{{
            "from_city": {city_name_1},
            "to_city": {city_name_2},
            "from_currency": {currency_1},
            "to_currency": {currency_2},
            "converted": {conversion_result}
        }}"""

    except Exception as e:
        return {"error": str(e)}

    # if city_name_1 is not None and amount is None and city_name_2 is None:
    #     country_code = _,country_code,_,_ = get_place_id(city_name_1)
    #     currency_info = get_currency_from_country_code(country_code)
    #     return "currency for city_name_1 will be {currency_info}"
    # elif city_name_1 is not None and amount is not None and city_name_2 is not None:
    #     country_code_1 = _,country_code,_,_ = get_place_id(city_name_1)
    #     country_code_2 = _,country_code,_,_ = get_place_id(city_name_2)
    #     currency_info_1 = get_currency_from_country_code(country_code_1)
    #     currency_info_2 = get_currency_from_country_code(country_code_2)
    #     currancy_conversion =get_convert_currancy(amount,currency_info_1,currency_info_2)
    #     return "currancy conversion and exchange rate will be {currancy_conversion}"



def get_currency_from_country_code(country_code):
    """
    Given a 2-letter country code (e.g. 'IN', 'US'), returns the currency code and symbol.
    """
    try:
        url = f"https://restcountries.com/v3.1/alpha/{country_code}"
        # url = f"https://restcountries.com/v3.1/currency/{currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        currencies = data[0].get("currencies", {})

        # The 'currencies' field is a dict with the currency code as key
        for code, info in currencies.items():
            return {
                "currency_code": code,
                "currency_name": info.get("name"),
                "currency_symbol": info.get("symbol")
            }
        return {"error": "Currency data not available."}

    except Exception as e:
        return {"error": str(e)}
def get_exchange_rate():
    pass

def get_convert_currancy(amount, from_currency, to_currency):
    currancy_url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(currancy_url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        rate = data["rates"].get(to_currency)
        if rate:
            converted = amount * rate
            return {
                "from": f"{amount} {from_currency}",
                "to": f"{converted:.2f} {to_currency}",
                "rate": rate
            }
        else:
            return {"error": f"Conversion rate for {to_currency} not found."}
# Example usage
# x = get_place_id('pune')
country,country_code,placeid,coordinates = get_place_id('dubai')
# country_code = "IN"  # Example from Geoapify for UAE
currency_info = get_currency_from_country_code(country_code)
print(currency_info)
y=get_convert_currancy(10,currency_info['currency_code'],'INR')
print(y)