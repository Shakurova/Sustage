from elasticsearch import Elasticsearch
from yandex_translate import YandexTranslate
import requests, re
import json
from sustage_score import get_sustage_score
from sustage_main import get_sustage_score_2
from basket import get_product_metadata


class Person:
    def __init__(self):
        # self.sustage_score = 0
        self.meat_free = Badges('meat_free')
        self.alchohol_free = Badges('alcohol_free')
        self.nutrition = Badges('nutrition')    # healthy choices badge
        self.ingredient = Badges('ingredient')  # sustainable ingredients
        self.processing = Badges('processing')  # processed_free
        self.sugar_free = Badges('sugar_free', 14)
        self.sustainable_brand = Badges('sustainable_brand')
        self.organic_brand = Badges('organic_brands')
        self.raw = Badges('raw', 10)
        self.fish_free = Badges('fish_free')
        self.dairy_free = Badges('dairy_free')
        self.plastic_bag_free = Badges('plastic_bag_free')
        self.package_free = Badges('plastic_free')

        self.organic_cert = Badges('organic_cert')
        self.fair_trade_cert = Badges('fair_trade')
        self.local_cert = Badges('local_cert')
        self.cruelty_free_cert = Badges('cruelty_free')
        self.animal_welfare_cert = Badges('animal_welfare_cert')
        self.environmentally_friendly_cert = Badges('environmentally_friendly_brand')
        self.recyclable_cert = Badges('recyclable_cert')
        self.plastic_free_cert = Badges('plastic_free_cert')

        # self.discount = 0
    def reprJSON(self):
        return dict(meat_free = self.meat_free, alchohol_free = self.alchohol_free, nutrition = self.nutrition, ingredient = self.ingredient, processing = self.processing, sugar_free = self.sugar_free, sustainable_brand = self.sustainable_brand, organic_brand = self.organic_brand, raw = self.raw, fish_free = self.fish_free, dairy_free = self.dairy_free, plastic_bag_free = self.plastic_bag_free, package_free = self.package_free, organic_cert = self.organic_cert, fair_trade_cert = self.fair_trade_cert, local_cert = self.local_cert, cruelty_free_cert = self.cruelty_free_cert, animal_welfare_cert = self.animal_welfare_cert, environmentally_friendly_cert = self.environmentally_friendly_cert, recyclable_cert = self.recyclable_cert, plastic_free_cert = self.plastic_free_cert)
        # self.discount = 0

    def badges_update(self, purchase_summary):
        """If a person gets the badge"""
        for top_el in ['sugar_free', 'raw', 'processing', 'package_free', 'sustainable_brand']:
            if self.top(purchase_summary.purchase_array, top_el):
                self.__dict__[top_el].bvalue_increment()
        for all_el in ['meat_free', 'alchohol_free', 'fish_free', 'dairy_free', 'plastic_bag_free']:
            if self.all(purchase_summary.purchase_array, all_el):
                self.__dict__[all_el].bvalue_increment()
            else:
                self.__dict__[all_el].bvalue_decrement()
        for any_el in ['nutrition', 'ingredient', 'organic_brand',
                       'organic_cert', 'fair_trade_cert', 'local_cert', 'cruelty_free_cert', 'animal_welfare_cert',
                       'environmentally_friendly_cert', 'recyclable_cert', 'plastic_free_cert']:
            if self.any(purchase_summary.purchase_array, any_el):
                self.__dict__[any_el].bvalue_increment()
        for behaviour in purchase_summary.__dict__:
            if behaviour != 'purchase_array':
                self.__dict__[behaviour].enlight_badge()

    def top(self, purchase_array, top_key):
        """If more than 30% of one purchase"""
        sum_True = sum([1 for item in purchase_array if item[top_key] == True])
        if float(sum_True) / len(receipt_data) > 0.3:
            return True
        return False

    def all(self, purchase_array, all_key):
        """If all in one purchase"""
        sum_True = sum([1 for item in purchase_array if item[all_key] == True])
        if sum_True == len(receipt_data):
            return True
        return False

    def any(self, purchase_array, any_key):
        """If any in one purchase"""
        sum_True = sum([1 for item in purchase_array if item[any_key] == True])
        if sum_True > 0:
            return True
        return False


class Purchase:
    def __init__(self, receipt_data):
        """If purchase was sustainable"""
        self.meat_free = False
        self.alchohol_free = False
        self.nutrition = False
        self.ingredient = False
        self.processing = False
        self.sugar_free = False #self.top(receipt_data, 6)
        self.sustainable_brand = False
        self.organic_brand = False
        self.raw = False
        self.fish_free = False  # top(receipt)
        self.dairy_free = False
        self.plastic_bag_free = False
        self.package_free = False  #False

        self.organic_cert = False
        self.fair_trade_cert = False
        self.local_cert = False
        self.cruelty_free_cert = False
        self.animal_welfare_cert = False
        self.environmentally_friendly_cert = False
        self.recyclable_cert = False
        self.plastic_free_cert = False

        self.check_purchase(receipt_data)

    def check_purchase(self, receipt_data):
        self.purchase_array = []
        for item_ean in receipt_data:
            if get_product_metadata(item_ean)['results']:
                sustage_dict = get_sustage_score(item_ean)
                sustage_dict_2 = get_sustage_score_2(item_ean)
                # matching
                for key in self.__dict__:
                    if key == 'organic_cert' and sustage_dict_2['raw']:
                        self.__dict__[key] = True if sustage_dict_2['organic_cert'] else False
                    elif key.endswith('_cert'):
                        for cert_descr in sustage_dict['certificates']:
                            key_set = re.findall(key[:-5], cert_descr)
                            self.__dict__[key] = True if key_set else False
                    else:
                        try:
                            if key in sustage_dict:
                                self.__dict__[key] = sustage_dict[key]
                        except:
                            if key in sustage_dict_2:
                                self.__dict__[key] = sustage_dict_2[key]
            # purchase_array.append(list(self.__dict__.values()))
            self.purchase_array.append(self.__dict__)


class Badges:
    def __init__(self, descr, treshold=3):
        self.description = descr
        self.treshold = treshold
        self.value = 0
        self.usable = False

    def bvalue_increment(self):
        """We found the badge behaviour in the receipt."""
        self.value += 1

    def bvalue_decrement(self):
        self.value = 0

    def enlight_badge(self):
        if self.value == self.treshold:
            self.usable = True

    def reprJSON(self):
        return dict(description=self.description, treshold=self.treshold, value=self.value, usable=self.usable)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


def test(person):
    for name in person.__dict__:
        badge = person.__dict__[name]
        try:
            print(badge.description, badge.value, badge.usable)
        except:
            print(name, badge)


if __name__ == "__main__":
    es = Elasticsearch('http://elastic:changeme@178.62.228.32:9200/')
    translate = YandexTranslate(
        'trnsl.1.1.20181124T220557Z.41ae0122588afa8e.054e4360b2ef5e7d597dc25883db22527dd8efa4')

    key = '0187dc68f47e49e9b97fc765bfd56716'
    content_type = 'application/json'

    receipt_data = ['7622300336738', '6410405060457', '6006258002388', '2000512100005']

    # we have data for one person for one purchase
    person = Person()
    purchase = Purchase(receipt_data)
    person.badges_update(purchase)
    # print("=" * 20)
    test(person)
    # purchase = Purchase(True, True, True, True)
    # person.badges_update(purchase)
    # print("="*20)
    # test(person)
    # purchase = Purchase(True, False, True, False)
    # person.badges_update(purchase)
    # print("="*20)
    # test(person)


def save_receipt(receipts):
    person = Person()
    purchase = Purchase(receipts)
    person.badges_update(purchase)
    return person

