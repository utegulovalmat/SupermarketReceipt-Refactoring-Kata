import pytest

from model_objects import Discount
from receipt_printer import ReceiptPrinter
from receipt import Receipt, ReceiptItem


@pytest.fixture
def sample_receipt(apples, toothbrush):
    receipt = Receipt()
    receipt.add_product(apples, 3.5, 10, 35)
    receipt.add_product(toothbrush, 1, 0.99, 0.99)
    receipt.add_discount(Discount(apples, "cheap apples", -10))
    return receipt


def test_print_receipt(sample_receipt):
    printer = ReceiptPrinter()
    expected_result = """apples                             35.00
  10.00 * 3.500
toothbrush                          0.99
cheap apples (apples)             -10.00

Total:                             25.99
"""
    result = printer.print_receipt(sample_receipt)
    assert result == expected_result


def test_print_receipt_item(apples):
    printer = ReceiptPrinter()
    item = ReceiptItem(apples, quantity=2, price=1.0, total_price=2.0)
    expected_result = """apples                              2.00
  1.00 * 2.000
"""
    result = printer.print_receipt_item(item)
    assert result == expected_result
