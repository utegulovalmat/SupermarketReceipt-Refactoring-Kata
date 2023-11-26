import pytest

from model_objects import Discount
from receipt import Receipt


def test_reciept(receipt, apples, toothbrush):
    receipt.add_product(apples, 3.5, 10, 35)
    receipt.add_product(toothbrush, 1, 0.99, 0.99)
    receipt.add_discount(Discount(apples, "cheap apples", -10))
    assert len(receipt.items) == 2
    assert len(receipt.discounts) == 1
    assert pytest.approx(receipt.total_price(), 0.01) == 25.99


def test_empty_receipt(receipt):
    assert receipt.total_price() == 0
