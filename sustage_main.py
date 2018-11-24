import pandas as pd

from pricing import get_products_from_store
from basket import put_item_into_basket, get_basket, get_product_metadata, get_total_price, apply_badge_discount

key = '0187dc68f47e49e9b97fc765bfd56716'
basket_id = '39693627'
basket_token = '1c2429dc3069a743980419d3b2350905fada2702'
content_type = 'application/json'

store_id_example = 'K171'
limit = 1
ean = None
offset = None

meat = ['pekoni', 'nauta', 'broileri', 'kinkku savustettu', 'kinkku keitetty', 'lammas', 'makkara', 'pihvi', 'vasikka']

scored_brands = pd.read_csv('good_brands.csv')

def main():
    print(get_product_metadata("6410402027521")['results'][0].keys())
    for k in get_product_metadata("6410402027521")['results'][0]:
        print(k, get_product_metadata("6410402027521")['results'][0][k])
        print('-'*10)

def badges(product='6410402027521'):
    positive = ['buy_organic', 'fair_trade', 'buy_local', 'is_seasonable', '']
    negative = ['meat_free', 'no_plastic', ]

    data = get_product_metadata(product)

    # Product Info
    brand = data['results'][0]['brand']
    attributes = data['results'][0]['attributes']
    ean = data['results'][0]['ean']
    category = data['results'][0]['category']
    subcategory = data['results'][0]['subcategory']
    segment = data['results'][0]['segment']

    # Badges Sustainability
    # True means good
    sustainable_brand = brand in scored_brands['Brand']
    #meat_free = all([True for word in subcategory if word not in meat])
    fresh, meat_free, fish_free, dairy_free = product_category_check(data)
    print(fresh, meat_free, fish_free, dairy_free)
    no_plastic = 'if there is no plastic bag in the list of your purchases'
    is_seasonable = ''
    fair_trade = ''
    buy_local = ''
    packaged_food = ''
    buy_organic = ''

    # Badges Health
    no_salt = ''
    alchohol_free = data['results'][0]['isAlcohol'] == False

    # return True, False, ...

def product_category_check(product):
    # default  = [False, False, False, False]
    pr_id = product["results"][0]["category"]["id"]

    categories = ['8', '13', '14', '15']

    checked = [True if cat == pr_id else False for cat in categories]

    return tuple(checked)



if __name__ == '__main__':
    badges()

    # print(get_products_from_store(store_id_example, 2))
    # print(put_item_into_basket(basket_id, basket_token, '0000040052441', 1, 1))
    # print(get_basket(basket_id, basket_token))
    # print(get_product_metadata("6410402027521"))
    # basj = get_basket(basket_id, basket_token)
    # print("Total price of the current basket is:", get_total_price(basj))
    # print(apply_badge_discount(get_total_price(basj), 7))
