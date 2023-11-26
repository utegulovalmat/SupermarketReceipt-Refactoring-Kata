from unittest import mock
from model_objects import Offer, SpecialOfferType
from teller import Teller


def test_teller(catalog, shopping_cart, apples):
    with mock.patch("shopping_cart.ShoppingCart.handle_offers") as mock_handle_offers:
        # Given
        catalog.add_product(product=apples, price=10)
        teller = Teller(catalog)
        shopping_cart.add_item_quantity(apples, 3.5)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)

        # When
        receipt = teller.checks_out_articles_from(shopping_cart)

        # Then
        assert mock_handle_offers.call_count == 1
        assert teller.catalog == catalog
        assert isinstance(teller.offers[apples], Offer)
