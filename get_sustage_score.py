from elasticsearch import Elasticsearch
from basket import get_product_metadata
import requests


es = Elasticsearch('http://elastic:changeme@178.62.228.32:9200/')

key = '0187dc68f47e49e9b97fc765bfd56716'
content_type = 'application/json'

ean = '7622300336738'


def get_sustage_score(ean):
    market_name = get_product_metadata(ean)['results'][0]['marketingName']['english']

    res = es.search(index="groceries", body=
    {
        "query": {
            "more_like_this": {
                "fields": ["name", "category_display_name", "category_link_name"],
                "like": market_name,
                "min_term_freq": 1,
                "max_query_terms": 4
            }
        }
    })

    hit = res['hits']['hits'][0]['_source']
    print(hit['name'])
    print(hit['scores'])
    upc = hit['upc']
    try:
        print(hit['cerifications'])
    except:
        pass
    try:
        print(hit['brand_name'])
    except:
        pass

    # Get additional info
    response = requests.get('http://api.ewg.org/food/' + upc + '?uuid=ddf62941-8f87-4b3e-bb4e-e5c48947d490')
    data = response.json()
    print(data["brand_name"])
    print(data["nutrients"]["has_added_sugar"])
    print("-" * 10)
    for page in data["page_details"]:
        if page["positive_negative"] in ['negative', 'positive']:
            print(page["positive_negative"])
            print(page["summary_text"])


if __name__ == '__main__':
    get_sustage_score(ean)


# res = es.search(index="groceries", body={"query": {"match": {"upc": "044000052881"}}})
# print(res)
# print("=" * 20)
# neat_res = res['hits']['hits'][0]['_source']
# print(neat_res['name'])
# print(neat_res['upc'])
# print(neat_res['category_display_name'])
# print(neat_res['category_link_name'])
# print(neat_res['category_groups'])
# print(neat_res['scores'])
# print("=" * 20)
# print(get_product_metadata(ean)['results'][0]['marketingName']['english'])
# print(get_product_metadata(ean)['results'][0]['ean'])
# print(get_product_metadata(ean)['results'][0]['category'])
# print(get_product_metadata(ean)['results'][0]['subcategory'])
