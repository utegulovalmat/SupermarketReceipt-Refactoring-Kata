import pytest
import math
from model_objects import Offer, Product, ProductQuantity, SpecialOfferType, Discount
from shopping_cart import ShoppingCart

from receipt import Receipt


@pytest.fixture
def sample_catalog(catalog, apples, toothbrush):
    catalog.add_product(apples, 10)
    catalog.add_product(toothbrush, 0.99)
    return catalog


def test_add_item(shopping_cart, apples):
    shopping_cart.add_item(apples)

    print(shopping_cart.items)
    assert len(shopping_cart.items) == 1
    assert shopping_cart.product_quantities[apples] == 1.0


def test_add_item_quantity(shopping_cart, apples):
    shopping_cart.add_item_quantity(apples, 2.0)
    print(shopping_cart.items)

    assert len(shopping_cart.items) == 1
    assert shopping_cart.product_quantities[apples] == 2.0


def test_handle_offers_three_for_two(catalog, shopping_cart, receipt, apples):
    catalog.add_product(apples, 10)
    shopping_cart.add_item_quantity(apples, 3.0)
    offers = {apples: Offer(SpecialOfferType.THREE_FOR_TWO, apples, 0)}
    receipt.add_product(apples, 3, 10, 30)

    shopping_cart.handle_offers(receipt, offers, catalog)

    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].description == "3 for 2"
    assert math.isclose(receipt.total_price(), 20.0, abs_tol=0.01)


def test_handle_offers_ten_percent_discount(catalog, shopping_cart, receipt, apples):
    catalog.add_product(apples, 10)
    shopping_cart.add_item_quantity(apples, 3.0)
    offers = {apples: Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)}
    receipt.add_product(apples, 3, 10, 30)

    shopping_cart.handle_offers(receipt, offers, catalog)

    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].product == apples
    assert receipt.discounts[0].description == "10.0% off"
    assert receipt.discounts[0].discount_amount == -3
    assert math.isclose(receipt.total_price(), 27, abs_tol=0.01)


def test_handle_offers_two_for_amount(catalog, shopping_cart, receipt, apples):
    """Probably ShoppingCart.handle_offers logic for SpecialOfferType.TWO_FOR_AMOUNT has a bug, when using / instead of //.
    Updated it for testing purposes."""
    catalog.add_product(product=apples, price=10)
    shopping_cart.add_item_quantity(product=apples, quantity=3.0)
    offers = {
        apples: Offer(
            offer_type=SpecialOfferType.TWO_FOR_AMOUNT, product=apples, argument=15.0
        )
    }
    receipt.add_product(product=apples, quantity=3.0, price=10, total_price=30)

    shopping_cart.handle_offers(receipt, offers, catalog)

    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].product == apples
    assert receipt.discounts[0].description == "2 for 15.0"
    assert receipt.discounts[0].discount_amount == -5
    assert math.isclose(receipt.total_price(), 25.0, abs_tol=0.01)


def test_handle_offers_five_for_amount(catalog, shopping_cart, receipt, apples):
    catalog.add_product(product=apples, price=10)
    shopping_cart.add_item_quantity(product=apples, quantity=6.0)
    offers = {
        apples: Offer(
            offer_type=SpecialOfferType.FIVE_FOR_AMOUNT, product=apples, argument=25.0
        )
    }
    receipt.add_product(product=apples, quantity=6.0, price=10, total_price=60)

    shopping_cart.handle_offers(receipt, offers, catalog)

    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].product == apples
    assert receipt.discounts[0].description == "5 for 25.0"
    assert receipt.discounts[0].discount_amount == -25
    assert math.isclose(receipt.total_price(), 35.0, abs_tol=0.01)
