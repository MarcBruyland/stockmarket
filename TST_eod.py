import requests
from dotenv.main import load_dotenv
import os

load_dotenv()
API_KEY = os.environ['API_KEY']

params = {
  'access_key': API_KEY
}

api_result = requests.get('http://api.marketstack.com/v1/tickers/SOF.XBRU/eod', params)

api_response = api_result.json()
print(api_response)

for k, v in api_response['data'].items():
    print(k,v)

sym = api_response['data']['symbol']
result = {}
for dic in api_response['data']['eod']:
    try:
        dt = dic['date'][:10]
        clo = dic['close']
        vol = dic['volume']
        exchange = dic['exchange']
        result[dt] = {'close': clo, 'volume': vol, 'exchange': exchange }
    except:
        print(dic)

myKeys = list(result.keys())
myKeys.sort()
sorted_result = {k: result[k] for k in myKeys}

for k, v in sorted_result.items():
    print(k, v)