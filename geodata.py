import requests
import json
import sys



#key values obtained for each location in the GeoData API dict_keys(['addressZH', 'nameZH', 'x', 'y', 'nameEN', 'addressEN'])
loc_name = input()
url = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch"
response = requests.get(url=url,params={"q": loc_name})
response_json = response.json()
print(response)
print(response_json)
print(response_json[-1].keys())
