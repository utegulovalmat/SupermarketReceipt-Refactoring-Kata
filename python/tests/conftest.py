import pytest
from catalog import SupermarketCatalog
from model_objects import Product, ProductUnit
from receipt import Receipt
from shopping_cart import ShoppingCart


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products = {}
        self.prices = {}

    def add_product(self, product, price):
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product):
        return self.prices[product.name]


@pytest.fixture
def toothbrush():
    return Product("toothbrush", ProductUnit.EACH)


@pytest.fixture
def apples():
    return Product("apples", ProductUnit.KILO)


@pytest.fixture
def catalog():
    return FakeCatalog()


@pytest.fixture
def shopping_cart():
    return ShoppingCart()


@pytest.fixture
def receipt():
    return Receipt()
