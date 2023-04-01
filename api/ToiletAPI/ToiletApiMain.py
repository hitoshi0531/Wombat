"""
This API works as follows:
1. Receive a HTTP request, and then get the address which is embeded in the request body.
2. Setting the received address as a parameter, call Google Maps API (GeoCoding API), then get laitude and longitude
3. Call the National Public Toilet API and get the public toilet dataset
4. Sort the toilet dataset by the distance from the latitude and longitude by Google Maps API
5. Return the top 15 itmes of sorted list
"""

#Import FastAPI from fastapi, JSONResponse from starlette.responses
from fastapi import FastAPI
from starlette.responses import JSONResponse


app = FastAPI()

#Root function
@app.get("/")
def read_root():
    return {"Hello": "World"}

#Function for just checking health
@app.get('/health', status_code=200)
def healthcheck():
    return 'This API is all ready to go!'


#Call Google Maps API(GeoCoding)
import requests

def get_lat_lng(address):
    api_key = "YOUR_API_KEY"
    url = f"<https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}>"
    response = requests.get(url)
    response_json = response.json()
    lat = response_json["results"][0]["geometry"]["location"]["lat"]
    lng = response_json["results"][0]["geometry"]["location"]["lng"]
    return lat, lng

#Call Google Maps API(GeoCoding)
import requests

def get_toilet_data(lat, lng):
    url = f"<https://toiletmap.gov.au/api/search?lat={lat}&lng={lng}&distance=10000&maxResults=100>"
    response = requests.get(url)
    response_json = response.json()
    return response_json["results"]

#Sort the toilet dataset by distance from the latitude and longitude by Google Maps API
def sort_by_distance(toilet_data, lat, lng):
    def distance(toilet):
        return ((toilet["latitude"] - lat)**2 + (toilet["longitude"] - lng)**2)**0.5
    toilet_data.sort(key=distance)
    return toilet_data

#Return the top 15 items of the sorted list
@app.post("/toilet_info/")
def get_toilet_info(address: str):
    lat, lng = get_lat_lng(address)
    toilet_data = get_toilet_data(lat, lng)
    sorted_toilet_data = sort_by_distance(toilet_data, lat, lng)
    return sorted_toilet_data[:15]
