from elasticsearch import Elasticsearch
from basket import get_product_metadata
from yandex_translate import YandexTranslate
import requests, re
from sustage_score import get_sustage_score


class Person:
    def __init__(self):
        # self.sustage_score = 0
        self.meat_free = Badges('meat_free')
        self.alchohol_free = Badges('alcohol_free')
        self.buy_local = Badges('local')
        self.packaged_food = Badges('packaged_food')
        self.nutrition = Badges('nutrition')
        self.ingredient = Badges('ingredient')
        self.processing = Badges('processing')
        self.added_sugar = Badges('added_sugar')
        self.organic_cert = Badges('organic_cert')
        self.fair_trade_cert = Badges('fair_trade')
        self.local_cert = Badges('local_cert')
        self.cruelty_free_cert = Badges('cruelty_free')
        self.animal_welfare_cert = Badges('animal_welfare_cert')

    def badges_update(self, purchase_summary):
        """If a person gets the badge"""
        for behaviour in purchase_summary.__dict__:
            if purchase_summary.__dict__[behaviour]:
                # conditionally more complex later
                self.__dict__[behaviour].bvalue_increment()
            else:
                if behaviour in ["meat_free", "packaged_food"]:
                    self.__dict__[behaviour].bvalue_decrement()
            self.__dict__[behaviour].enlight_badge()


class Purchase:
    def __init__(self, mf=False, af=False, bl=False, pf=False):#, receipt_data):
        """If purchase was sustainable"""
        self.meat_free = mf
        self.alchohol_free = af
        self.buy_local = bl
        self.packaged_food = pf
        self.nutrition = False
        self.ingredient = False
        self.processing = False
        self.added_sugar = False
        self.organic_cert = False
        self.fair_trade_cert = False
        self.local_cert = False
        self.cruelty_free_cert = False
        self.animal_welfare_cert = False

        self.check_purchase()#receipt_data)


    def check_purchase(self):#, receipt_data):
        # for item in receipt_data:
        item_ean = '6410405060457'
        sustage_dict = get_sustage_score(item_ean)
        # matching
        for key in self.__dict__:
            if key.endswith('_cert'):
                for cert_descr in sustage_dict['certificates']:
                    key_set = re.findall(key[:-5], cert_descr)
                    self.__dict__[key] = True if key_set else False
            try:
                self.__dict__[key] = sustage_dict[key]
            except:
                pass


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
    purchase = Purchase(True, True, False, True) #Purchase(receipt_data)
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





