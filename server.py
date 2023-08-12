import requests
from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
from dotenv.main import load_dotenv
import os
from image_maker import create_image

load_dotenv()
API_KEY = os.environ['API_KEY']  # api key for https://marketstack.com/

app = Flask(__name__)
bootstrap = Bootstrap(app)

def sort_dic_on_keys(dic, direction="ascending"):
    my_keys = list(dic.keys())
    if direction == "ascending":
        my_keys.sort()
    elif direction == "descending":
        my_keys.sort(reverse=True)
    sorted_dic = {k: dic[k] for k in my_keys}
    return sorted_dic

def get_eod_data(ticker):
    params = {
        'access_key': API_KEY
    }
    api_result = requests.get(f"http://api.marketstack.com/v1/tickers/{ticker}/eod", params)

    api_response = api_result.json()
    print(api_response)

    for k, v in api_response['data'].items():
        print(k, v)

    name = api_response['data']['name']
    sym = api_response['data']['symbol']
    result = {}
    exchange = "???"
    for dic in api_response['data']['eod']:
        try:
            dt = dic['date'][:10]
            clo = dic['close']
            vol = dic['volume']
            exchange = dic['exchange']
            result[dt] = {'close': clo, 'volume': vol, 'exchange': exchange}
        except:
            print(dic)

    sorted_result = sort_dic_on_keys(result)
    return name, sym, sorted_result, exchange

def get_cur_of_exchange(mic):
    cur = "???"
    params = {
        'access_key': API_KEY
    }
    api_result = requests.get(f'http://api.marketstack.com/v1/exchanges/{mic}', params)

    api_response = api_result.json()
    print(api_response)
    return api_response['name'], api_response['currency']['code']

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/exchanges")
def get_exchanges():
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
    sorted_result = sort_dic_on_keys(result)

    return render_template("exchanges.html", result=sorted_result)

@app.route("/currencies")
def get_currencies():
    params = {
        'access_key': API_KEY
    }
    api_result = requests.get('http://api.marketstack.com/v1/currencies', params)
    api_response = api_result.json()
    print(api_response)

    result = {}
    for dic in api_response['data']:
        try:
            curr = dic['code']
            if curr:
                if curr not in result:
                    result[curr] = {}
                result[curr]['name'] = dic['name']
                result[curr]['symbol'] = dic['symbol']
        except:
            print(dic)
    print(result)
    sorted_result = sort_dic_on_keys(result)
    print(sorted_result)
    return render_template("currencies.html", result=sorted_result)

@app.route("/tickers")
def get_tickers():
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
    sorted_result1 = sort_dic_on_keys(result)

    for country, dic_country in sorted_result1.items():
        sorted_dic_country = sort_dic_on_keys(dic_country)
        sorted_result1[country] = sorted_dic_country

    print(sorted_result1)

    sorted_result2 = sort_dic_on_keys(result2)
    print(sorted_result2)
    return render_template("tickers.html", result1=sorted_result1, result2=sorted_result2)



@app.route("/eod_via_form", methods=["POST"])
def get_eod_via_form():
    print(request.method)
    ticker = request.form["ticker"]
    print(ticker)
    name, sym, sorted_result, mic = get_eod_data(ticker)
    exchange, cur = get_cur_of_exchange(mic)
    filename = create_image(name, sym, sorted_result, exchange, cur)
    return render_template("eod.html", result=sorted_result, name=name, ticker=sym, filename=filename)

@app.route("/eod/<ticker>", methods=["GET"])
def get_eod(ticker):
    print(ticker)
    name, sym, sorted_result, mic = get_eod_data(ticker)
    exchange, cur = get_cur_of_exchange(mic)
    filename = create_image(name, sym, sorted_result, exchange, cur)
    return render_template("eod.html", result=sorted_result, name=name, ticker=sym, filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run(debug=True)
