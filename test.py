import requests
import json
print(json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/country/canada').text))