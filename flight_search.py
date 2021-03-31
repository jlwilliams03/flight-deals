import requests
from flight_data import FlightData

# Kiwi Partners Flight Search API:  https://partners.kiwi.com
KIWI_API_KEY = "PIZ0h-th0mfjVHWSiBdxIUi17nvZZ-Gp"
FROM_CITY = "DFW"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        pass

    def get_location_code(self, city):
        kiwi_locations_url = "https://tequila-api.kiwi.com"
        kiwi_query_endpoint = "/locations/query?"
        headers = {"apikey": KIWI_API_KEY}
        query = {
            "term"          : city,
            "location_types": "city"
        }
        response = requests.get(url=kiwi_locations_url + kiwi_query_endpoint, headers=headers,
                                params=query)
        results = response.json()["locations"]
        try:
            code = results[0]["code"]
            return code
        except IndexError:
            print(f"No IATA code found for {city}")
            return None

    def search_flight(self, from_city_code, to_city_code, from_date, to_date):
        kiwi_search_url = "https://tequila-api.kiwi.com/v2"
        kiwi_search_endpoint = "/search"
        headers = {"apikey": KIWI_API_KEY}
        query = {

            "fly_from"          : from_city_code,
            "fly_to"            : to_city_code,
            "date_from"         : from_date.strftime("%d/%m/%Y"),
            "date_to"           : to_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to"  : 28,
            "flight_type"       : "round",
            "one_for_city"      : 1,
            "max_stopovers"     : 0,
            "curr"              : "USD"

        }
        response = requests.get(url=kiwi_search_url + kiwi_search_endpoint, headers=headers,
                                params=query)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for destination {to_city_code}")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["cityFrom"],
            origin_airport=data["cityCodeFrom"],
            destination_city=data["cityTo"],
            destination_airport=data["cityCodeTo"],
            leave_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        return flight_data
