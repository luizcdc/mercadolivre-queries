import unittest
import ML_scraper
from random import choice
from pickle import load
with open("categories.pickle", "rb") as cat:
    backup_CATS = load(cat)


class TestCategories(unittest.TestCase):
    """Tests the integrity of the categories database.

    What is tested
    ---------------
    - first category is "Todas" (all) with number 0.0
    - all categories' numbers are unique and ordered
    - first child of each parent starts with 1
    - types of categories' contents are correct

    Note
    ----
    Every test that alters the 'cats' copy of the categories must set
    the class variable last_test_altered_cats as true. Using that infor-
    mation, setUp will restore cats to the original value.

    We can expect, if test_todas_inserted_in_0,
    test_all_unique_and_ordered and test_children_start_with_one are
    successful, that any category can be obtained by simply indexing
    'CATS' and its elements, except when it does not exist. The "Todas"
    (all) can be obtained by indexing CATS[0][0] for the parent and
    CATS[0][1][0] for the child, while any other category can be ob-
    tained by indexing CATS[parent_number][0] for the parent and
    CATS[parent_number][1][child_number-1] for the child.
    """
    last_test_altered_cats = False
    cats = backup_CATS.copy()
    # Copying 'CATS' to allow destructive operations. It will be
    # checked for integrity during SetUp()

    def setUp(self):
        if self.last_test_altered_cats == True:
            self.cats = backup_CATS.copy()
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
        has only one child and it gets tested in test_todas_inserted_in_0
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

        The meaning of type consistency here is the conformity to speci-
        fication of types. This tests simply randomly select categories
        and tests if each and every element that compose those categori-
        es' infor mation is of the appropriate type.
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
        # handled exclusively by setUp() and the other tests
        pass


class TestGetCat(unittest.TestCase):
    """Tests the behaviour of the function get_cat

    What is tested
    --------------
    - input -> expected output cases
    - return type is (str,str)
    - get_cat does not return an empty subdomain
    - get_cat raises ValueError if non-existent category is requested
    - get_cat returns values that are present on CATS
    - get_cat does not modify CATS in any way

    Details
    -------
    test_expected_outputs and test_raises_ValueError_if_not_existent
    rely on the property of retrieving the category by indexing, which
    is only guaranteed if TestCategories passes completely.
    """

    def test_expected_outputs(self):
        """Tests some input-output examples"""
        pass

    def test_returns_correct_types(self):
        """Tests if get_cat returns a tuple of strings

        Randomly chooses categories from CATS database, and checks if
        get_cat returns always two strings.
        """
        pass

    def test_subdomain_not_empty(self):
        """Asserts that the subdomain returned is never empty"""
        pass

    def test_raises_ValueError_if_not_existent(self):
        """Asserts that a non-existent input category raises a ValueError

        This design choice, instead of defaulting for the "Todas" (all)
        category was deemed better because it signals when something is
        not working better than just ignoring it and performing a valid
        search despite not being able to input the right category.
        """
        pass

    def test_returned_values_in_CATS(self):
        """Tests that the result is from CATS and not from other source

        This test assures that the returned values were extracted from
        CATS and didn't get altered by the function in any way.
        """
        pass

    def test_doesnt_modify_CATS(self):
        """Tests that get_cat does not modify the content of CATS"""
        pass


class TestGetLink(unittest.TestCase):
    """Tests the behaviour of the function get_link

    What is tested
    --------------
    - return type is str
    - get_link strips irrelevant information
    - get_link doesn't return something that wasn't contained
    in the tag
    - get_link returns an empty string if something went wrong

    Details
    -------
    The 'stripping' test relies on the fact that, at the time of rele-
    ase of the first version of this program, every valid MercadoLivre
    product page link in its minimal version ends with "MLB1231231232"
    or "-_JM" (1231231232 standing for any arbitrary number).
    """

    def test_returns_string(self):
        """Tests that the return type is str"""
        pass

    def test_link_is_from_tag(self):
        """Tests that the final link is contained in the tag's text"""
        pass

    def test_link_stripped_correctly(self):
        """Tests if link was stripped of trailing irrelevant information"""
        pass

    def test_failure_returns_empty_string(self):
        """Tests the return in case of failure

        The failure of this function, characterized by the extraction of
        a link that's not correctly ended or an exception being raised
        during it's execution, must return an empty string, which allows
        for the functions that rely on it to handle it accordingly.
        """
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
