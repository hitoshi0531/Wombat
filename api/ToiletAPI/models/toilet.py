# Import module for API requests
import requests

# Import math module for calculating distance
import math

# Import the module for reading the .env file
import os
from dotenv import load_dotenv

# Loaing the content of .env
load_dotenv('.env')

# Turn address into latitude and longitude
def get_lat_lng(address):
    google_maps_api_key = os.environ['GOOGLE_MAPS_API_KEY']
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, google_maps_api_key)
    response = requests.get(url)
    response_json = response.json()
    lat = response_json["results"][0]["geometry"]["location"]["lat"]
    lng = response_json["results"][0]["geometry"]["location"]["lng"]
    return lat, lng

# Call Public Toilet API
def get_toilet_data(lat, lng, state):
    url = 'https://data.gov.au/data/api/3/action/datastore_search?resource_id=34076296-6692-4e30-b627-67b7c4eb1027&limit=1000&filters={}'.format("{\"State\":"+"\""+state+"\""+"}")
    response = requests.get(url)
    response_json = response.json()
    return response_json

# Sort the toilet dataset by distance from the latitude and longitude by Google Maps API
def sort_by_distance(toilet_data, lat, lng):
    # Convert dictionary data of toilet_data into list data (toilet_list)
    toilet_list = list(toilet_data.items())

    # Extract all toilet informatin list out of toilet_list
    toilet_info_list = toilet_list[2][1]['records']

    # Convert latitude and longitude from string into float with each element of the toilet_info list
    for toilet_info in toilet_info_list:
        toilet_info['Latitude'] = float(toilet_info['Latitude'])
        toilet_info['Longitude'] = float(toilet_info['Longitude'])

    # Calculating distance in meter by Hybeny's Distance Formula 
    def calculate_distance(lat, lng, toilet_info_lat, toilet_info_lng):
        """
        pole_radius = 6356752.314245
        equator_radius = 6378137.0
        # Convert to radians
        lat = math.radians(lat)
        lng = math.radians(lng)
        toilet_info_lat = math.radians(toilet_info_lat)
        toilet_info_lng = math.radians(toilet_info_lng)
        lat_difference = lat - toilet_info_lat
        lon_difference = lng - toilet_info_lng
        lat_average = (lat + toilet_info_lat) / 2
        e2 = (math.pow(equator_radius, 2) - math.pow(pole_radius, 2)) / math.pow(equator_radius, 2)
        w = math.sqrt(1- e2 * math.pow(math.sin(lat_average), 2))
        m = equator_radius * (1 - e2) / math.pow(w, 3)
        n = equator_radius / w
        distance = math.sqrt(math.pow(m * lat_difference, 2) + math.pow(n * lon_difference * math.cos(lat_average), 2))
        return distance
        """
        return (((toilet_info_lat - lat)**2 + (toilet_info_lng - lng)**2)**0.5)*100000


    for toilet_info in toilet_info_list:
        toilet_info['distance'] = calculate_distance(lat, lng, toilet_info['Latitude'], toilet_info['Longitude'])
        
    # Sort the list by distance in descending order
    toilet_info_list_sorted = sorted(toilet_info_list, key=lambda x: x['distance'])
    return toilet_info_list_sorted

