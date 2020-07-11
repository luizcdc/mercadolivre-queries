import unittest
import ML_scraper
from random import choice
from pickle import load
with open("categories.pickle", "rb") as cat:
    CATS = load(cat)


class TestCategories(unittest.TestCase):
    last_test_altered_cats = False
    cats = CATS.copy()
    # Copying 'CATS' to allow destructive operations. It will be
    # checked for integrity during SetUp()
    """Tests the integrity of the categories database.

    Every test that alters the 'cats' copy of the categories must set
    the class variable last_test_altered_cats as true.
    """

    def setUp(self):
        if self.last_test_altered_cats == True:
            self.cats = CATS.copy()
        self.last_test_altered_cats = False

    def test_todas_inserted_in_0(self):
        """cats[0] must be "All Categories" ("Todas")"""
        self.assertTrue("todas" in self.cats[0][0][1].lower())
        self.assertEqual(self.cats[0][0][0], 0)
        self.__class__.last_test_altered_cats = False

    def test_all_unique_and_ordered(self):
        """Tests for uniqueness and order of categories' X.Y IDs

        All parent categories' numbers must be unique, and inside the
        list of children of a parent category, every element must have
        a unique number as well. They should be in crescent order.

        self.cats[0] doesn't need to pass this test because it is hardcoded,
        has only one child and gets tested in todas_inserted_in_0
        anyway.
        """
        for former_parent, curr_parent in zip(self.cats, self.cats[1:]):
            self.assertEqual(former_parent[0][0] + 1, curr_parent[0][0])
            for former_child, curr_child in zip(curr_parent[1], curr_parent[1][1:]):
                self.assertEqual(former_child['number'] + 1, curr_child['number'])
        self.__class__.last_test_altered_cats = False

    def test_children_start_with_one(self):
        """Tests if the 1st element of each parent category is number 1

        The number here referred is child['number']. Together with
        all_unique_and_ordered() and todas_inserted_in_0(), this test
        is the final assurance that the categories database is ordered
        and unique, always starting from the number 1 (except in
        category 'Todas').
        """
        for curr_parent in self.cats[1:]:
            self.assertEqual(curr_parent[1][0]['number'], 1)

    def test_consistent_with_types(self):
        """Tests randomly some categories for type consistency

        Using random.choice, select 10 parent categories, and test 2
        child categories of them for type consistency.
        """
        for _ in range(10):
            curr_parent = choice(self.cats)
            for _ in range(2):
                curr_child = choice(curr_parent[1])
                self.assertEqual(type(curr_parent[0][0]), int)
                self.assertEqual(type(curr_parent[0][1]), str)
                self.assertEqual(type(curr_child['number']), int)
                self.assertEqual(type(curr_child['name']), str)
                self.assertEqual(type(curr_child['suffix']), str)
                self.assertEqual(type(curr_child['subdomain']), str)
        self.__class__.last_test_altered_cats = False

    def tearDown(self):
        # if tearDown() is later implemented, don't set
        # last_test_altered_cats to anything here, it needs to be
        # handled uniquely by setUp()
        pass


class TestGetCat(unittest.TestCase):
    """Tests the behaviour of the function get_cat"""

    def test_returns_correct_types(self):
        pass

    def test_subdomain_not_empty(self):
        pass

    def test_raises_ValueError_if_not_existent(self):
        pass

    def test_returned_values_in_CATS(self):
        pass

    def test_doesnt_modify_CATS(self):
        pass


class TestGetLink(unittest.TestCase):
    """Tests the behaviour of the function get_link"""
    def test_link_valid():
        pass


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


class TestIsReputable(unittest.TestCase):
    """Tests the behaviour of the function is_reputable"""


class TestGetAllProducts(unittest.TestCase):
    """Tests the behaviour of the function get_all_products"""


class TestGetSearchPages(unittest.TestCase):
    """Tests the behaviour of the function get_search_pages"""


class TestGetParameters(unittest.TestCase):
    """Tests the behaviour of the function get_parameters"""


class TestMLQuery(unittest.TestCase):
    """Tests the behaviour of the function ML_query"""


if __name__ == "__main__":
    unittest.main()
