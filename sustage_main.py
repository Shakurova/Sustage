import pandas as pd
import json
from pricing import get_products_from_store
from basket import put_item_into_basket, get_basket, get_product_metadata, get_total_price, apply_badge_discount

key = '0187dc68f47e49e9b97fc765bfd56716'
basket_id = '39693627'
basket_token = '1c2429dc3069a743980419d3b2350905fada2702'
content_type = 'application/json'

eans = ['2000604700007',
'2000503600002',
'2000528000009',
'2000818700008',
'2000614400003',
'6410405060457',
'2000585400002',
'2000503600002',
'2000686300003',
'2000528900002',
'2000511100006',
'2000510800006',
'2000511700008',
'6006258002388',
'2000388400001',
'2000512100005',
'6410402008896',
'2000642500003',
'2000650800003',
'6410405054623',
'8436008522145',
'6410405114471',
'6410402008773',
'6410405046109',
'6410405041548',
'2000600100009',
'2000507900009',
'6416046670000',
'2000530600006',
'6416046652129',
'2000798000006',
'2000592600006',
'6410402008933',
'6410405082657',
'6410402011742',
'6410405048561',
'6408430004010',
'5760466987806',
'2350460300003',
'6407880083347',
'6407810016094']


scored_brands = pd.read_csv('good_brands.csv')
with open('finnish_brands.json', 'r', encoding='utf-8') as data_file:
    finnish_brands = json.load(data_file)

organic_list = ['Luomutarkastajan hyväksyntä', 'EU:n luomutunnus (lehti)', 'Muu kansallinen luomumerkki', 'Luomumerkki (Aurinko)', 'Krav Merkki', 'BIO Merkki', 'ECOCERT certificate', 'Luomumerkki (Leppäkerttu)', 'Demeter-merkki']
env_list = ['FSC-sertifikaatti (Forrest Stewardship Council)', 'Pohjoismainen ympäristömerkki (Joutsen)', 'Soil Association -merkki', 'Rainforest alliance certified (Sammakko-merkki)', 'Forest stewardship council mix', 'EU:n ympäristömerkki (EU-kukka)', 'UTZ_certification', 'PEFC-logo', 'EKO']
fair_list = ['Reilu Kauppa', 'Fair For Life']

def main(product='721865095627'):
    print(get_product_metadata(product)['results'][0].keys())
    for k in get_product_metadata(product)['results'][0]:
        print(k, get_product_metadata(product)['results'][0][k])
        print('-'*10)


def product_category_check(product):
    """ Check for fish, meat, milk."""
    pr_id = product["results"][0]["category"]["id"]
    categories = ['13', '14', '15']
    checked = [False if cat == pr_id else True for cat in categories]

    return tuple(checked)

def product_category_check_fresh(product):
    """ Check for greens. """
    pr_id = product["results"][0]["category"]["id"]

    return True if pr_id == '8' else False

def get_brand_name(s1, s2):
    """ Return brand. """
    out = ""
    for word in range(len(s1.split())):
        w1 = s1.split()[word]
        w2 = s2.split()[word]
        if w1 == w2:
            out += w1 + ' '
            continue
        else:
            break
    return out


def fill_in_tx(data):
    """ Fill in certification labels. """
    main_d = {}
    attributes = data['results'][0]['attributes']
    for t in ['TX_KIEOMI', 'TX_YMPMER', 'TX_PAKMER', 'TX_RAVOMI']:
        if t in attributes:
            relevant = attributes[t]
            big_value = relevant['value']
            all_values = []
            if type(big_value) == list:
                for v in big_value:
                    explanation_value = v['explanation']['finnish']
                    all_values.append(explanation_value)
            else:
                explanation_value = big_value['explanation']['finnish']
                all_values.append(explanation_value)
            main_d[t] = all_values
    return main_d


def badges(product='7622300336738'):
    outputs = {}

    positive = ['buy_organic', 'fair_trade', 'buy_local', 'is_seasonable', '']
    negative = ['meat_free', 'no_plastic']

    data = get_product_metadata(product)

    # Product Info
    name = data['results'][0]['labelName']['english']
    brand = data['results'][0]['brand'] if 'brand' is data['results'][0] else ''
    finnish = data['results'][0]['labelName']['finnish']
    swedish = data['results'][0]['labelName']['swedish']
    brand = brand if brand else get_brand_name(finnish, swedish)
    ean = data['results'][0]['ean']
    print('NAME', name, brand, ean)

    # Badges
    TX_dict = fill_in_tx(data)
    TX_KIEOMI = TX_dict['TX_KIEOMI'] if 'TX_KIEOMI' in TX_dict else ''
    TX_YMPMER = TX_dict['TX_YMPMER'] if 'TX_YMPMER' in TX_dict else ''
    TX_PAKMER = TX_dict['TX_PAKMER'] if 'TX_PAKMER' in TX_dict else ''
    TX_RAVOMI = TX_dict['TX_RAVOMI'] if 'TX_RAVOMI' in TX_dict else ''

    outputs['alchohol_free'] = data['results'][0]['isAlcohol'] == False
    outputs['sustainable_brand'] = brand in scored_brands['Brand']
    outputs['buy_organic'] = 'Organic' in finnish_brands[brand.lower()] if brand.lower() in finnish_brands else None
    outputs['fresh'] = product_category_check_fresh(data)  # healthy choices
    outputs['meat_free'] = product_category_check(data)[0]
    outputs['fish_free'] = product_category_check(data)[1]
    outputs['dairy_free'] = product_category_check(data)[2]
    outputs['no_plastic_bag'] = ean != '6410405187734'
    outputs['packaged_food_good'] = data['results'][0]['pricingUnit'] != 'pussi'
    outputs['plastic_waste_free'] = 'Muovipakkausjäte' not in TX_KIEOMI

    outputs['organic_cert'] = any([True for o in TX_YMPMER if o in organic_list])
    outputs['fair_trade_cert'] = any([True for o in TX_YMPMER if o in fair_list])
    outputs['env_friendly_cert'] = any([True for o in TX_YMPMER if o in env_list])
    outputs['recyclable_cert'] = 'Materiaalikierrätys' in TX_KIEOMI or 'Kierrätysmerkki' in TX_KIEOMI

    return outputs

if __name__ == '__main__':
    for e in eans:
        print(badges(product=e))
