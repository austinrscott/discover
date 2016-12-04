from enum import Enum
from random import random, randrange


class Resources(Enum):

    Food = 1
    Water = 2
    Gold = 3


class ResourcePrice:

    def __init__(self, res, price):
        self.res = res
        self.price = price

    @staticmethod
    def get_random_price():
        res = Resources(randrange(len(Resources)))
        price = randrange(100)
        return ResourcePrice(res, price)


class Market:

    def __init__(self):
        self.prices = {res: randrange(100) for res in list(Resources)}

    def get_sell_price(self, res, amount):
        return self.prices[res] * amount

    def display(self):
        for key in self.prices:
            print("{0} for ${1}".format(key, self.prices[key]))

class Inventory:

    def __init__(self):
        self.inventory = {res: 0 for res in list(Resources)}

    def __add_resource(self, res, amount):
        self.inventory[res] += amount

    def give(self, res, amount, inventory_to):
        """
        :type res: Resources
        :type amount: int
        :type inventory_to: Inventory
        """

        self.__add_resource(res, -amount)
        inventory_to.__add_resource(res, amount)

    def display(self):
        for key in self.inventory:
            print("{0} : {1}".format(key, self.inventory[key]))

class Settlement:

    def __init__(self, name):
        self.name = name
        self.market = Market()
        self.inv = Inventory()

    def get_sell_price(self, res, amount):
        return self.market.get_sell_price(res, amount)

    def sell(self, res, amount, my_inventory):
        my_inventory.give(res, amount, self.inv)
        return self.get_sell_price(res, amount)

    def display(self):
        self.inv.display()
        self.market.display()


class Ship:

    def __init__(self, name, pos):
        self.name = name
        self.inv = Inventory()
        self.pos = pos

    def move(self, new_pos):
        self.pos = new_pos

    def get_pos(self):
        return self.pos


port_angeles = Settlement("Port Angeles")
ship_inv = Inventory()

print(port_angeles.sell(Resources.Gold, 10, ship_inv))

port_angeles.display()
print("-----------------------------------")
ship_inv.display()

