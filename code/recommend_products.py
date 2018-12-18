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
                'time': timestamp_for_logging(),
                'status': 'All Good Here!'}
    return Response(json.dumps(response), status=200)


def build_products_collection():
    print(timestamp_for_logging(), ': build_products_collection')
    active_ingredient1 = {'name': 'Active ingredient 1'}
    active_ingredient2 = {'name': 'Active ingredient 2'}
    active_ingredient3 = {'name': 'Active ingredient 3'}
    active_ingredient4 = {'name': 'Active ingredient 4'}

    active_ingredients_collection_1 = [active_ingredient1, active_ingredient2]
    active_ingredients_collection_2 = [active_ingredient3, active_ingredient4]

    product1 = {
        "product": {
                       "name": "Product Name 1",
                       "active_ingredients": active_ingredients_collection_1
                   }
    }

    product2 = {
        "product": {
            "name": "Product Name 2",
            "active_ingredients": active_ingredients_collection_2
        }
    }

    japanese_beetle_product = {
        "product": {
            "name": "Japanese Beetle Killer",
            "active_ingredients": active_ingredients_collection_1
        }
    }

    green_stink_bug_product = {
        "product": {
            "name": "Green Stink Bug Killer",
            "active_ingredients": active_ingredients_collection_1
        }
    }

    corn_earworm_product = {
        "product": {
            "name": "Corn Earworm Killer",
            "active_ingredients": active_ingredients_collection_1
        }
    }

    green_apple_aphid_product = {
        "product": {
            "name": "Green Apple Aphid Killer",
            "active_ingredients": active_ingredients_collection_1
        }
    }

    bean_leaf_beetle_product = {
        "product": {
            "name": "Bean Leaf Beetle Killer",
            "active_ingredients": active_ingredients_collection_1
        }
    }

    japanese_beetle_products = {'pest': 'japanese_beetle', 'products': [japanese_beetle_product, product1]}
    green_stink_bug_products = {'pest': 'green_stink_bug', 'products': [green_stink_bug_product, product2, product1]}
    corn_earworm_products = {'pest': 'corn_earworm', 'products': [corn_earworm_product, product2, product1, product1]}
    green_apple_aphid_products = {'pest': 'green_apple_aphid', 'products': [green_apple_aphid_product, product2, product1, product2]}
    bean_leaf_beetle_products = {'pest': 'bean_leaf_beetle', 'products': [bean_leaf_beetle_product, product2]}

    all_products = {
        "products": [japanese_beetle_products,
                     green_stink_bug_products,
                     corn_earworm_products,
                     green_apple_aphid_products,
                     bean_leaf_beetle_products
                     ]
    }

    print(json.dumps(all_products))
    return all_products


def get_products_for_pest(pest):
    print(timestamp_for_logging(), ': get_products_for_pest, pest =', pest)
    all_products = build_products_collection().get('products')
    print('all products: ',all_products)

    for p in list(all_products):
        print('p: ', p)
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
