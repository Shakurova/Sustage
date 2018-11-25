from elasticsearch import Elasticsearch
from basket import get_product_metadata
from yandex_translate import YandexTranslate
import requests, re
from sustage_score import get_sustage_score
from sustage_main import get_sustage_score_2


class Person:
    def __init__(self):
        # self.sustage_score = 0
        self.meat_free = Badges('meat_free')
        self.alchohol_free = Badges('alcohol_free')
        self.nutrition = Badges('nutrition')    # healthy choices badge
        self.ingredient = Badges('ingredient')  # sustainable ingredients
        self.processing = Badges('processing')  # processed_free
        self.sugar_free = Badges('sugar_free')
        self.sustainable_brand = Badges('sustainable_brand')
        self.organic_brand = Badges('organic_brands')
        self.raw = Badges('raw')
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

        self.discount = 0

    def badges_update(self, purchase_summary):
        """If a person gets the badge"""
        negs = ['meat_free', 'alchohol_free', 'fish_free', 'dairy_free', 'plastic_bag_free']
        for behaviour in purchase_summary.__dict__:
            if purchase_summary.__dict__[behaviour]:
                # conditionally more complex later
                self.__dict__[behaviour].bvalue_increment()
            else:
                if behaviour in negs:
                    self.__dict__[behaviour].bvalue_decrement()
            self.__dict__[behaviour].enlight_badge()


class Purchase:
    def __init__(self):#, receipt_data):
        """If purchase was sustainable"""
        self.meat_free = False
        self.alchohol_free = False
        self.nutrition = False
        self.ingredient = False
        self.processing = False
        self.sugar_free = False
        self.sustainable_brand = False
        self.organic_brand = False
        self.raw = False
        self.fish_free = False
        self.dairy_free = False
        self.plastic_bag_free = False
        self.package_free = False

        self.organic_cert = False
        self.fair_trade_cert = False
        self.local_cert = False
        self.cruelty_free_cert = False
        self.animal_welfare_cert = False
        self.environmentally_friendly_cert = False
        self.recyclable_cert = False
        self.plastic_free_cert = False

        self.check_purchase()#receipt_data)

    def check_purchase(self):#, receipt_data):
        # for item in receipt_data:
        item_ean = '6410405060457'
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
                    self.__dict__[key] = sustage_dict[key]
                except:
                    self.__dict__[key] = sustage_dict_2[key]


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

    # we have data for one person for one purchase
    person = Person()
    test(person)
    purchase = Purchase() #Purchase(receipt_data)
    person.badges_update(purchase)
    print("=" * 20)
    test(person)
    # purchase = Purchase(True, True, True, True)
    # person.badges_update(purchase)
    # print("="*20)
    # test(person)
    # purchase = Purchase(True, False, True, False)
    # person.badges_update(purchase)
    # print("="*20)
    # test(person)





