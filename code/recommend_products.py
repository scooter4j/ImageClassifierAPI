# Product Recommendations API
# authored by Scott Queen
# start date: 12/17/18
#
#
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, Response, request
from flask_basicauth import BasicAuth

import datetime
import time
import json
import threading

products_for_pest = {}

# App Globals (do not edit)
app = Flask(__name__)


def timestamp_for_logging():
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    return ts


@app.route('/health')
def health_check():
    print(timestamp_for_logging(), ': request made to health_check')
    response = {'service': 'ProductRecommendationService',
                'version': '1.1.0',
                'time': timestamp_for_logging(),
                'status': 'All Good Here!'}
    return Response(json.dumps(response), status=200)


def build_products_collection():
    print(timestamp_for_logging(), ': build_products_collection')
    cyfluthrin = {'name': 'Cyfluthrin'}
    pyrethroid = {'name': 'Pyrethroid'}
    pyrethrins = {'name': 'Pyrethrins'}
    acetamiprid = {'name': 'Acetamiprid'}
    esfenvalerate = {'name': 'Esfenvalerate'}
    indoxacarb = {'name': 'Indoxacarb'}
    lambda_cyhalothrin = {'name': 'Lambda-cyhalothrin'}
    cypermethrin = {'name': 'Cypermethrin'}
    very_cold_temps = {'name': 'Very Cold Temps'}

    tombstone_helios = {
        "name": "Tombstone Helios",
        "active_ingredients": [cyfluthrin]
    }

    stryker = {
        "name": "Stryker",
        "active_ingredients": [pyrethrins]
    }

    tristar = {
        "name": "Tristar",
        "active_ingredients": [acetamiprid]
    }

    onslaught = {
        "name": "Onslaught",
        "active_ingredients": [esfenvalerate]
    }

    avaunt = {
        "name": "Avaunt",
        "active_ingredients": [indoxacarb]
    }

    pyganic = {
        "name": "PyGanic",
        "active_ingredients": [pyrethrins]
    }

    demand_cs = {
        "name": "Demand CS",
        "active_ingredients": [lambda_cyhalothrin]
    }

    demonmax = {
        "name": "DemonMax",
        "active_ingredients": [cypermethrin]
    }

    arilon = {
        "name": "Arilon",
        "active_ingredients": [indoxacarb]
    }

    karate = {
        "name": "Karate",
        "active_ingredients": [pyrethroid]
    }

    winter_freeze = {
        "name": "Cold Harsh Winter",
        "active_ingredients": [very_cold_temps]
    }

    japanese_beetle_products = {
        'pest': 'japanese beetle',
        'products': [tombstone_helios, karate]
    }

    green_stink_bug_products = {
        'pest': 'green stink bug',
        'products': [demand_cs, demonmax, arilon]
    }

    corn_earworm_products = {
        'pest': 'corn earworm',
        'products': [onslaught, stryker, avaunt]
    }

    green_apple_aphid_products = {
        'pest': 'green apple aphid',
        'products': [pyganic, onslaught, stryker]
    }

    bean_leaf_beetle_products = {
        'pest': 'bean leaf beetle',
        'products': [tombstone_helios, stryker, tristar]
    }

    furry_lipped_rib_borer_products = {
        'pest': 'furry lipped rib borer',
        'products': [winter_freeze]
    }

    all_products = {
        "products": [japanese_beetle_products,
                     green_stink_bug_products,
                     corn_earworm_products,
                     green_apple_aphid_products,
                     bean_leaf_beetle_products,
                     furry_lipped_rib_borer_products
                     ]
    }

    print(json.dumps(all_products))
    return all_products


def get_products_for_pest(pest):
    print(timestamp_for_logging(), ': get_products_for_pest, pest =', pest)
    all_products = build_products_collection().get('products')

    for p in list(all_products):
        if p['pest'] == pest:
            return p

    return {}


@app.route('/rp', methods=['GET'])
def recommend_products():
    pest = request.args.get('pest')
    print(timestamp_for_logging(), ': request made to recommend_products for ', pest)
    products_for_pest = get_products_for_pest(pest)
    return Response(json.dumps(products_for_pest), status=200)


def run_web_server():
    print(timestamp_for_logging(), ': starting the web server')
    app.run(host='0.0.0.0', debug=False)


if __name__ == "__main__":
    t = threading.Thread(target=run_web_server, args=())
    t.daemon = True
    t.start()

    # keep the app running so the web-server thread will stay alive
    while True:
        time.sleep(1)
