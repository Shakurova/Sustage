import requests
import json

key = '0187dc68f47e49e9b97fc765bfd56716'
basket_id = '39693627'
basket_token = '1c2429dc3069a743980419d3b2350905fada2702'
content_type = 'application/json'


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


def generate_random_basket(store_id, how_many_products):
	pass



