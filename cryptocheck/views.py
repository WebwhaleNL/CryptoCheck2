###########################################
### Setup ###
###########################################

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# for enabling sending emails from here
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# import settings.py
from django.conf import settings

# CMC specific
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



###########################################

# This is where the logic goes on how to handle certain routes


def home(request):
    return HttpResponse('<h1>Cryptocheck Home</h1>')






  



# Route to index HTML
def index(request):
    print('Hallo Max!')
    return render(request, 'cryptocheck/index.html')



@csrf_exempt
def getCMCdata(request, coinRankID):

    print("Route getCMCdata is now loaded")

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    currency = 'USD'

    # Settings for data import
    parameters = {
        'start':coinRankID, #getting data from specified coin rank
        'limit':'1', # only getting data from this specific coin
        'convert':currency,
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ced57759-8eb5-4de1-875e-221f3d4ef252',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    # Now get specific data from dict that you need
    timestamp = data['status']['timestamp']
    coin_name = data['data'][0]['name']
    coin_cir_supply = data['data'][0]['circulating_supply']
    coin_cmc_rank = data['data'][0]['cmc_rank']
    coin_price = data['data'][0]['quote'][currency]['price']
    coin_market_cap = data['data'][0]['quote'][currency]['market_cap']

    
    #debugging
    print("Route getCMCdata is now complete")

    # Now return some data
    data = {
        'timestamp': timestamp,
        'coin_name': coin_name,
        'coin_cir_supply': coin_cir_supply,
        'coin_cmc_rank': coin_cmc_rank,
        'coin_price': coin_price,
        'coin_market_cap': coin_market_cap,
    }

    return JsonResponse(data)