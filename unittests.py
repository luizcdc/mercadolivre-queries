import unittest
import ML_scraper

with open("categories.pickle", "rb") as cat:
    CATS = load(cat)


class TestCategories(unittest.TestCase):
    """Tests the integrity of the categories database."""


class TestGetLink(unittest.TestCase):
    """Tests the behaviour of the function get_link"""


class TestGetTitle(unittest.TestCase):
    """Tests the behaviour of the function get_title"""


class TestGetPrice(unittest.TestCase):
    """Tests the behaviour of the function get_price"""


class TesteGetPicture(unittest.TestCase):
    """Tests the behaviour of the function get_picture"""


class TestIsNoInterest(unittest.TestCase):
    """Tests the behaviour of the function is_no_interest"""


class TesteHasFreeShipping(unittest.TestCase):
    """Tests the behaviour of the function has_free_shipping"""


class TestIsInSale(unittest.TestCase):
    """Tests the behaviour of the function is_in_sale"""


class TestGetAllProducts(unittest.TestCase):
    """Tests the behaviour of the function get_all_products"""


class TestIsReputable(unittest.TestCase):
    """Tests the behaviour of the function is_reputable"""


class TestPrintProduct(unittest.TestCase):
    """Tests the behaviour of the function print_product"""


class TestPrintCats(unittest.TestCase):
    """Tests the behaviour of the function print_cats"""


class TestGetCat(unittest.TestCase):
    """Tests the behaviour of the function get_cat"""


class TestGetSearchPages(unittest.TestCase):
    """Tests the behaviour of the function get_search_pages"""


class TestGetParameters(unittest.TestCase):
    """Tests the behaviour of the function get_parameters"""


class TestMLQuery(unittest.TestCase):
    """Tests the behaviour of the function ML_query"""
