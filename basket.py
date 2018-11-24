import requests
import json
from pricing import get_products_from_store
import random


key = '0187dc68f47e49e9b97fc765bfd56716'
basket_id = '39693627'
basket_token = '1c2429dc3069a743980419d3b2350905fada2702'
content_type = 'application/json'
otaniemi_store_id = 'K171'


def put_item_into_basket(basket_id, basket_token, product_ean, basket_item_id, how_many):

	headers = {'Ocp-Apim-Subscription-Key': key, 'x-basket-token': basket_token}

	body = {
  			"multiplier": how_many,
  			"item": product_ean
	}

	url = f'https://kesko.azure-api.net/baskets/{basket_id}/items/{basket_item_id}'

	r = requests.put(url, headers=headers, json=body)

	return json.loads(r.text)


# print(put_item_into_basket(basket_id, basket_token, '0000040052441', 1, 1))


def get_basket(basket_id, basket_token):

	url = f'https://kesko.azure-api.net/baskets/{basket_id}'

	headers = {'Ocp-Apim-Subscription-Key': key, 'x-basket-token': basket_token}

	r = requests.get(url, headers=headers)

	return json.loads(r.text)


# print(get_basket(basket_id, basket_token))


def get_product_metadata(product_ean):

	url = 'https://kesko.azure-api.net/v1/search/products'

	headers = {'Ocp-Apim-Subscription-Key': key, 'content-type': content_type}

	body = {
		"filters": {
        	"ean": product_ean
    		}
		}

	r = requests.post(url, headers=headers, json=body)

	return json.loads(r.text)


# print(get_product_metadata("6410402027521"))
	

def get_total_price(basket_json):

	total_price = basket_json['totalPrice']

	return total_price


# basj = get_basket(basket_id, basket_token)
# print("Total price of the current basket is:", get_total_price(basj))


def apply_badge_discount(current_price, discount_percentage):

	discount = current_price * (discount_percentage / 100)

	return float("{0:.2f}".format(current_price - discount))


# print(apply_badge_discount(get_total_price(basj), 7))



# We generate multiple user baskets: for first basket we create a few sustainable ones and a few non sustainable ones. 
# For the second basket we just fill it with random products. Then we apply the discounts from the first basket on 
# the second random one and show what happens with the discount.


def generate_random_basket(store_id, how_many_products, eans_pool):

	url = f'https://kesko.azure-api.net/baskets/{store_id}'

	headers = {'Ocp-Apim-Subscription-Key': key}

	r = requests.post(url, headers=headers)

	new_empty_basket = json.loads(r.text)

	basket_token = new_empty_basket['token']
	basket_longid = new_empty_basket['longId']

	for index, random_ean in enumerate(random.sample(eans_pool, how_many_products)):

		basket = put_item_into_basket(basket_longid, basket_token, random_ean, index, 1)

	return basket


# all_shop_eans = get_products_from_store("K171", 1, offset=0).keys()
# print(all_shop_eans)


def generate_basket_from_eans(eans_list, store_id):

	url = f'https://kesko.azure-api.net/baskets/{store_id}'

	headers = {'Ocp-Apim-Subscription-Key': key}

	r = requests.post(url, headers=headers)

	new_empty_basket = json.loads(r.text)

	basket_token = new_empty_basket['token']
	basket_longid = new_empty_basket['longId']

	for index, ean in enumerate(eans_list):

		basket = put_item_into_basket(basket_longid, basket_token, ean, index, 1)

	return basket



# print(generate_random_basket(otaniemi_store_id, 10, get_products_from_store("K171", 1000, offset=0).keys()))

print(generate_basket_from_eans(['2000528000009', '2000511100006', '6410405082657', 
								 '2000600100009', '2000511700008'], otaniemi_store_id))


# 	{
#   "storeId": "K171",
#   "storeName": "K-MARKET OTANIEMI",
#   "checkoutDone": false,
#   "token": "3b75afea154de60d711a5b8ccacc4de2559562db",
#   "items": [],
#   "longId": "09180575",
#   "shortId": "0844",
#   "expires": "2018-11-25T15:13:52+00:00",
#   "modified": "2018-11-24T15:13:52+00:00",
#   "totalPrice": 0,
#   "totalPlussaPrice": 0
# }






