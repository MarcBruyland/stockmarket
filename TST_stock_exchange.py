import requests
from dotenv.main import load_dotenv
import os

load_dotenv()
API_KEY = os.environ['API_KEY']

params = {
  'access_key': API_KEY
}

api_result = requests.get('http://api.marketstack.com/v1/exchanges', params)

api_response = api_result.json()
print(api_response)

result = {}
for dic in api_response['data']:
    country = dic['country']
    acronym = dic['acronym']
    if country:
        if country not in result:
            result[country] = []
        if acronym:
            result[country].append(acronym)

myKeys = list(result.keys())
myKeys.sort()
sorted_result = {k: sorted(result[k]) for k in myKeys}

for k, v in sorted_result.items():
    print(k, v)