from elasticsearch import Elasticsearch
from basket import get_product_metadata
from yandex_translate import YandexTranslate
import requests

es = Elasticsearch('http://elastic:changeme@178.62.228.32:9200/')
translate = YandexTranslate(
            'trnsl.1.1.20181124T220557Z.41ae0122588afa8e.054e4360b2ef5e7d597dc25883db22527dd8efa4')

key = '0187dc68f47e49e9b97fc765bfd56716'
content_type = 'application/json'

ean = '6410405060457'


def get_sustage_score(ean):
    sustage_dict = {}

    try:
        market_name = get_product_metadata(ean)['results'][0]['marketingName']['english']
    except:
        fi_name = get_product_metadata(ean)['results'][0]['marketingName']['finnish']
        market_name = translate.translate(fi_name, 'fi-en')['text']

    res = es.search(index="groceries", body=
    {
        "min_score": 0.1,
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
    upc = hit['upc']
    # print(hit['name'])
    scores = hit['scores']
    # print(scores)
    sustage_dict['nutrition'] = True if scores['nutrition'] < 3.0 else False
    sustage_dict['ingredient'] = True if scores['ingredient'] < 3.0 else False
    sustage_dict['processing'] = True if scores['processing'] < 3.0 else False

    cert_d = {}
    try:
        for cert in hit['certifications']:
            cert_d[cert['description']] = cert['name']
        sustage_dict['certificates'] = cert_d
    except:
        pass
    # try:
    #     print(hit['brand_name'])
    # except:
    #     pass

    # Get additional info
    response = requests.get('http://api.ewg.org/food/' + upc + '?uuid=ddf62941-8f87-4b3e-bb4e-e5c48947d490')
    data = response.json()
    sustage_dict["sugar_free"] = data["nutrients"]["has_added_sugar"]
    # print("-" * 10)
    # for page in data["page_details"]:
    #     if page["positive_negative"] in ['negative', 'positive']:
    #         print(page["positive_negative"])
    #         print(page["summary_text"])

    return sustage_dict


if __name__ == '__main__':
    sustage_dict = get_sustage_score(ean)
    print(sustage_dict)


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
