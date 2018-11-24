
class Person:
    def __init__(self):
        # self.sustage_score = 0
        self.meat_free = Badges('meat_free')
        self.alchohol = Badges('alcohol')
        self.fair_trade = Badges('fair_trade')
        self.buy_local = Badges('local')
        self.packaged_food = Badges('packaged_food')
        # to be continued

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
    def __init__(self, mf=False, al=False, ft=False, bl=False, pf=False):#, receipt_data):
        """If purchase was sustainable"""
        self.meat_free = mf
        self.alchohol = al
        self.fair_trade = ft
        self.buy_local = bl
        self.packaged_food = pf

        # to be continued
        # self.check_purchase(receipt_data)

    # def check_purchase(self, receipt_data):
        # filling in every attribute


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
    # we have data for one person for one purchase
    person = Person()
    test(person)
    purchase = Purchase(True, True, False, True, False) #Purchase(receipt_data)
    person.badges_update(purchase)
    print("="*20)
    test(person)
    purchase = Purchase(True, True, True, True, True)
    person.badges_update(purchase)
    print("="*20)
    test(person)
    purchase = Purchase(True, False, True, False, False)
    person.badges_update(purchase)
    print("="*20)
    test(person)





