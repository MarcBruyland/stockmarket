import requests
from dotenv.main import load_dotenv
import os

load_dotenv()
API_KEY = os.environ['API_KEY']

params = {
  'access_key': API_KEY
}

api_result = requests.get('http://api.marketstack.com/v1/tickers', params)

api_response = api_result.json()
print(api_response)

result = {}
result2 = {}
for dic in api_response['data']:
    sym = dic['symbol']
    name = dic['name']
    country = dic['stock_exchange']['country']
    acronym = dic['stock_exchange']['acronym']
    if country not in result:
        result[country] = {}
    if acronym not in result[country]:
        result[country][acronym] = []
    result[country][acronym].append(sym)
    if sym in result2:
        print(f"double symbol: {sym} - see {country}, {acronym} and {result2[sym]}")
    else:
        result2[sym] = {'name': name, 'country': country, 'acronym': acronym}

myKeys = list(result.keys())
myKeys.sort()
sorted_result = {k: result[k] for k in myKeys}

for country, dic_country in sorted_result.items():
    myKeys = list(dic_country.keys())
    myKeys.sort()
    sorted_dic_country = {k: dic_country[k] for k in myKeys}
    for acronym, lst in sorted_dic_country.items():
        print(f"{country} - {acronym} - {sorted(lst)}")

print()

myKeys = list(result2.keys())
myKeys.sort()
sorted_result = {k: result2[k] for k in myKeys}

for k, v in sorted_result.items():
    print(k,v)