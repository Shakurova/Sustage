import requests
import json

content_type = 'application/json'
accept = content_type

key = '0187dc68f47e49e9b97fc765bfd56716'

headers = {'Ocp-Apim-Subscription-Key': key, 'accept': accept, 'content-type': content_type}

####### Store products
store_id_example = 'K171'
limit = 1
ean = None
offset = None
######


def get_products_from_store(store_id, limit, ean=None, offset=None):

	url = f'https://kesko.azure-api.net/v4/stores/{store_id_example}/products'

	payload = {'limit': str(limit), 'offset': str(offset)}

	r = requests.get(url, headers=headers, params=payload)

	return json.loads(r.text)


# print(get_products_from_store("K171", 1000, offset=0).keys())


def get_all_eans_otaniemi():
	return set(get_products_from_store("K171", 1000, offset=0).keys())

print(get_all_eans_otaniemi())
# def get_product_price(ean):




