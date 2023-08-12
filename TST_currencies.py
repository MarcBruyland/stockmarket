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
    try:
        curr = dic['currency']['code']
        if curr:
            if not curr in result:
                result[curr] = []
            result[curr].append(dic['name'])
    except:
        print(dic)

myKeys = list(result.keys())
myKeys.sort()
sorted_result = {k: sorted(result[k]) for k in myKeys}

for k, v in sorted_result.items():
    print(k, v)
