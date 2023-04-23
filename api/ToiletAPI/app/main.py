"""
This API works as follows:
1. Receive a HTTP request, and then get the address which is embeded in the request body.
2. Setting the received address as a parameter, call Google Maps API (GeoCoding API), then get laitude and longitude
3. Call the National Public Toilet API and get the public toilet dataset
4. Sort the toilet dataset by the order of the distance from the targeted location, calculated by the latitude and longitude
5. Return the top 15 itmes of sorted list
"""

#Import FastAPI from fastapi, JSONResponse from starlette.responses
from fastapi import FastAPI
from starlette.responses import JSONResponse
import sys
sys.path.append('../models/')
from toilet import get_lat_lng, get_toilet_data, sort_by_distance 

app = FastAPI()

#Root function
@app.get("/")
def read_root():
    return {"Hello": "World!!"}

#Function for just checking health
@app.get('/health', status_code=200)
def healthcheck():
    return 'This API is all ready to go!'

#Return the top 10 items of the sorted list
@app.get("/toilet_info/")
def get_toilet_info(address: str):
    lat, lng = get_lat_lng(address)
    # Identify the state included in the received address
    import re
    match = re.search(r"\bNSW\b|\bVIC\b|\bQLD\b|\bWA\b|\bSA\b|\bTAS\b|\bACT\b|\bNT\b", address)
    state = match.group()
    # Call the toilet data API
    toilet_data = get_toilet_data(lat, lng, state)
    # Sort the toilet data by distance
    toilet_info_list_sorted = sort_by_distance(toilet_data, lat, lng)
    return toilet_info_list_sorted[:10]
