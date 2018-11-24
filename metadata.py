import requests
import json
from pricing import get_products_from_store
from basket import get_product_metadata
import pandas as pd

key = '0187dc68f47e49e9b97fc765bfd56716'

otaniemi_store_id = 'K171'

content_type = 'application/json'
accept = content_type

relevant_keywords = ['TX_KIEOMI', 'TX_PAKMER', 'TX_RAVOMI', 'TX_YMPMER']


def get_relevant_metadata(product_ean):

	relevant_metadata = {}

	try:
		md = get_product_metadata(product_ean)['results'][0]

		marketing_name = md['marketingName']['finnish']

		attributes = md['attributes']
		# print(attributes)
		# print("+-+-+")
		# print(attributes['TX_KIEOMI'])

		for relevant_keyword in relevant_keywords:
			# print(relevant_keyword)
			try:
				relevant = attributes[relevant_keyword]
				# print(relevant)
				# print("-+-+-")
			except:
				continue

			explanation = relevant['explanation']['finnish']

			evs = []
			values = []
			abbs = []

			try:
				big_value = relevant['value']
				if type(big_value) == list:
					for v in big_value:
						explanation_value = v['explanation']['finnish']
						value = v['value']
						try:
							abbreviation = v['abbreviation']
						except:
							abbreviation = 'None'
						evs.append(explanation_value)
						values.append(value)
						abbs.append(abbreviation)
				else:
					explanation_value = big_value['explanation']['finnish']
					value = big_value['value']
					try:
						abbreviation = big_value['abbreviation']
					except:
						abbreviation = 'None'
			except:
				explanation_value = 'None'
				value = 'None'
				abbreviation = 'None'

			# print(relevant_keyword)
			# print("NAME", marketing_name, "EV:", explanation_value, "VAL:", value,
			# 	  "ABBR:", abbreviation, "EVS:", evs, "VALS:", values, "ABBS:", abbs)
			# print("-+-+-")

			if evs and abbs and values:
				relevant_metadata[relevant_keyword] = {"name": marketing_name, 
									   "numerical_values": values,
									   "abbreviations": abbs,
									   "explanation_values": evs}
			else:
				relevant_metadata[relevant_keyword] = {"name": marketing_name, 
									   "numerical_value": value,
									   "abbreviation": abbreviation,
									   "explanation_value": explanation_value}

		return relevant_metadata
	except:
		return None


current = 0
all_keys = []
for i in range(24):
	current += 1000
	all_store_products_info = get_products_from_store("N106", 1000, offset=current)
	all_store_product_eans = list(all_store_products_info.keys())
	all_keys = all_keys + all_store_product_eans

print("Done collecting all eans")
print("Total eans amount:", len(all_keys))

product_json = {}
for index, ean in enumerate(all_keys):
	if index % 500 == 0:
		print("Processed 500 eans")
	product_json[str(ean)] = get_relevant_metadata(str(ean))


with open('product_emblems_big.json', 'w') as outfile:
    json.dump(product_json, outfile)







