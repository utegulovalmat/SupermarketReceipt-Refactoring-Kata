import pytest

from model_objects import SpecialOfferType
from teller import Teller


def test_ten_percent_discount(catalog, toothbrush, apples, shopping_cart):
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    shopping_cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(shopping_cart)

    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)

    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity
