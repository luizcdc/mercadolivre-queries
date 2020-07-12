import unittest
import ML_scraper
from bs4 import BeautifulSoup
from random import choice, randint
from pickle import load

with open("categories.pickle", "rb") as cat:
    backup_CATS = load(cat)

product = """<li class="results-item highlighted article stack product "> <div class="rowItem item product-item highlighted item--stack new with-reviews to-item has-variations" id="MLB1543163640"><div class="item__image item__image--stack"> <div class="images-viewer" item-url="https://www.mercadolivre.com.br/iphone-11-128-gb-preto-4-gb-ram/p/MLB15149567?source=search#searchVariation=MLB15149567&amp;position=1&amp;type=product&amp;tracking_id=b008d681-98e3-4479-90c6-98bd291f30f6" item-id="MLB1543163640" product-id="MLB15149567"> <div class="image-content"> <a href="https://www.mercadolivre.com.br/iphone-11-128-gb-preto-4-gb-ram/p/MLB15149567?source=search#searchVariation=MLB15149567&amp;position=1&amp;type=product&amp;tracking_id=b008d681-98e3-4479-90c6-98bd291f30f6" class="figure item-image item__js-link"> <img class="lazy-load" width="160" height="160" alt="iPhone 11 128 GB Preto 4 GB RAM" src="https://http2.mlstatic.com/D_NQ_NP_678481-MLA42453875909_072020-V.webp"> </a> </div> </div></div><div class="item__info-container highlighted "> <div class="item__info item--show-right-col "> <div class="item__highlight__container"> <div class="item__highlight item__highlight--deal" style="color: rgb(255, 255, 255); background: rgb(52, 131, 250); --darkreader-inline-color:#e8e6e3; --darkreader-inline-bgimage: initial; --darkreader-inline-bgcolor:#0447ac;" data-darkreader-inline-color="" data-darkreader-inline-bgimage="" data-darkreader-inline-bgcolor=""> Enviando normalmente </div> </div><h2 class="item__title list-view-item-title"> <a href="https://www.mercadolivre.com.br/iphone-11-128-gb-preto-4-gb-ram/p/MLB15149567?source=search#searchVariation=MLB15149567&amp;position=1&amp;type=product&amp;tracking_id=b008d681-98e3-4479-90c6-98bd291f30f6" class="item__info-title"> <span class="main-title"> iPhone 11 128 GB Preto 4 GB RAM </span> </a> <div class="item__brand"> <a class="item__brand-link" href="https://loja.mercadolivre.com.br/fast-shop"> <span class="item__brand-title-tos"> por Fast Shop </span> </a> </div></h2> <div class="price__container"> <span class="price-old" itemprop="price-old"> <del> R$&nbsp;6.099 </del> </span><div class="item__price item__price-discount"> <span class="price__symbol">R$</span> <span class="price__fraction">4.629</span></div> <div class="item__discount ">24% OFF</div> </div> <div class="item__stack_column highlighted"> <div class="item__stack_column__info"> <div class="stack_column_item installments highlighted"><span class="item-installments free-interest"> <span class="item-installments-multiplier"> 12x </span> <span class="item-installments-price"> R$ 385 <sup class="installment__decimals">75</sup> </span> <span class="item-installments-interest"> sem juros </span></span> </div> <div class="stack_column_item status"> <div class="item__status"> <div class="item__condition"> </div> </div> </div> </div> </div> <div class="stack_colum_right without-attributes with-reviews"> <div class="item__reviews"> <div class="stars"> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> </div> <div class="item__reviews-total">232</div></div> <div class="stack_column_right__bottom item__has-variations"> <div class="variation-picker__container"> <div class="ui-dropdown custom"> <input type="checkbox" id="dropdown-variations-0" class="dropdown-trigger variation-picker__trigger" autocomplete="off" hidden="" data-id="MLB1543163640"> <label for="dropdown-variations-0" class="ui-dropdown__link"> <span class="variation-picker__label">Cor: </span> <span class="ui-dropdown__display variation-picker__label variation-picker__label-bold">Preto</span> <div class="ui-dropdown__indicator"></div> </label> <div class="ui-dropdown__content dropdown__variations-content variation-picker cursor-wait variation-picker__size-3" data-size="3"> <ul class=""> <li id="MLB15149567" class="attrBox skeleton__box--0 selected-option"> <img class="variation-picker__img" title="Preto" width="36" height="36" src="https://http2.mlstatic.com/D_Q_NP_857283-MLA42453875910_072020-S.webp"></li> <li id="MLB15149572" class="attrBox skeleton__box--3 "> <img class="variation-picker__img" title="(Product)Red" width="36" height="36" src="https://http2.mlstatic.com/D_Q_NP_608338-MLA42453875933_072020-S.webp"></li> <li id="MLB15149568" class="attrBox skeleton__box--5 "> <img class="variation-picker__img" title="Branco" width="36" height="36" src="https://http2.mlstatic.com/D_Q_NP_899930-MLA42453930760_072020-S.webp"></li></ul> </div> </div> </div> </div> </div> </div></div> <form class="item__bookmark-form" action="/search/bookmarks/MLB1543163640/make" method="post" id="bookmarkForm"> <button type="submit" class="bookmarks favorite " data-id="MLB1543163640"> <div class="item__bookmark"> <div class="icon"></div> </div> </button> <input type="hidden" name="method" value="add"> <input type="hidden" name="itemId" value="MLB1543163640"> <input type="hidden" name="_csrf" value="cbe9313a-32d9-4618-bc3d-c0bb7091ebce"> </form> </div></li>"""
product_tag = BeautifulSoup(product, "html.parser")
incorrect_tag = BeautifulSoup("<span class=\"price__symbol\">R$</span>",
                              "html.parser")
# this raw html was extracted from a listing of the iPhone 11. It was chosen be-
# cause usually an iPhone stays being commercialized for many years after its
# launch, meaning that is less likely that the link will break in the next 5
# years
print(ML_scraper.get_link(product_tag))
input()


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
        es' information is of the appropriate type.
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
    - get_cat does not modify CATS in any way

    Details
    -------
    test_expected_outputs and test_raises_ValueError_if_not_existent
    rely on the property of retrieving the category by indexing, which
    is only guaranteed if TestCategories passes completely.
    """
    @staticmethod
    def random_valid_category():
        """Helper method that returns data from a random valid category"""
        parent = choice(ML_scraper.CATS)
        child = choice(parent[1])
        return (f"{parent[0][0]}.{child['number']}",
                child["subdomain"], child["suffix"])

    def test_expected_outputs(self):
        """Tests if given category is retrieved consistently"""
        for _ in range(10):
            cat_code, subdomain, suffix = TestGetCat.random_valid_category()
            ret_subdomain, ret_suffix = ML_scraper.get_cat(cat_code)
            self.assertEqual(ret_subdomain, subdomain)
            self.assertEqual(ret_suffix, suffix)

    def test_returns_correct_types(self):
        """Tests if get_cat returns a tuple of strings

        Randomly chooses categories from CATS database, and checks if
        get_cat returns always two strings.
        """
        for _ in range(10):
            cat_code, _, _ = TestGetCat.random_valid_category()
            subdomain, suffix = ML_scraper.get_cat(cat_code)
            self.assertTrue(isinstance(subdomain, str))
            self.assertTrue(isinstance(suffix, str))

    def test_subdomain_not_empty(self):
        """Asserts that the subdomain returned is never empty"""
        for _ in range(10):
            cat_code, _, _ = TestGetCat.random_valid_category()
            subdomain, _ = ML_scraper.get_cat(cat_code)
            self.assertTrue(subdomain != "")

    def test_raises_ValueError_if_not_existent(self):
        """Asserts that a non-existent input category raises a ValueError

        This design choice, instead of defaulting for the "Todas" (all)
        category was deemed better because it signals when something is
        not working better than just ignoring it and performing a valid
        search despite not being able to input the right category.
        """
        for _ in range(10):
            with self.assertRaises(ValueError):
                ML_scraper.get_cat(f"{randint(50,10000)}.{randint(50,10000)}")

    def test_doesnt_modify_CATS(self):
        """Tests that get_cat does not modify the content of CATS"""
        for _ in range(10):
            cat_code, _, _ = TestGetCat.random_valid_category()
            ML_scraper.get_cat(cat_code)

        self.assertTrue(ML_scraper.CATS == backup_CATS)


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
        self.assertTrue(isinstance(ML_scraper.get_link(product_tag), str))

    def test_link_is_from_tag(self):
        """Tests that the final link is contained in the tag's text"""
        print(ML_scraper.get_link(product_tag))
        self.assertTrue(ML_scraper.get_link(product_tag) in product)

    def test_link_stripped_correctly(self):
        """Tests if link was stripped of trailing irrelevant information"""
        # TODO: IMPLEMENT
        pass

    def test_failure_returns_empty_string(self):
        """Tests the return in case of failure

        The failure of this function, characterized by the extraction of
        a link that's not correctly ended or an exception being raised
        during it's execution, must return an empty string, which allows
        for the functions that rely on it to handle it accordingly.
        """
        self.assertEqual(ML_scraper.get_link("some string"), "")
        self.assertEqual(ML_scraper.get_link(incorrect_tag), "")
        self.assertEqual(ML_scraper.get_link(123312), "")


class TestGetTitle(unittest.TestCase):
    """Tests the behaviour of the function get_title

    A title will always be a string, and it needs to be stripped of
    spaces in the beginning or the end. Failure to obtain the title of a
    product is not a fatal failure and for that reason, should not raise
    an exception, but simply return something that symbolizes this fai-
    lure.

    What is tested
    --------------
    - returned string correctly stripped
    - extracts correctly for a provided example
    - returns empty string in failure
    """


class TestGetPrice(unittest.TestCase):
    """Tests the behaviour of the function get_price

    A price must be stored as a couple (tuple) of ints, except when
    there was a failure to retrieve this information, in which case it
    is stored as (nan,nan), so that when sorting the list, no errors
    are raised, and the items that lack price are returned in the end
    of the list, independent of choice of ordering.

    What is tested
    --------------
    - type is (int,int) for provided example
    - value is correct for provided example
    - type is (float('nan'),float('nan')) on failure to extract
    """


class TestGetPicture(unittest.TestCase):
    """Tests the behaviour of the function get_picture

    A picture is stored as a hyperlink (str). Failure to retrieve a pic-
    ture of a product is not a fatal failure, and an empty string should
    be returned in case of failure.

    What is tested
    --------------
    - type is string
    - returned value is a hyperlink
    - returns empty string on failure
    - returns correctly for provided example
    """


class TestIsNoInterest(unittest.TestCase):
    """Tests the behaviour of the function is_no_interest

    What is tested
    --------------
    - return type is bool
    - in failure returns false
    - returns correctly for provided example
    """


class TestHasFreeShipping(unittest.TestCase):
    """Tests the behaviour of the function has_free_shipping

    What is tested
    --------------
    - return type is bool
    - failure returns false
    - returns correctly for provided example
    """


class TestIsInSale(unittest.TestCase):
    """Tests the behaviour of the function is_in_sale

    What is tested
    --------------
    - return type is bool
    - failure returns false
    - returns correctly for provided example
    """


class TestIsReputable(unittest.TestCase):
    """Tests the behaviour of the function is_reputable

    What is tested
    --------------
    - return type is bool
    - failure returns false
    - returns correctly for provided example (may break if provided
    example of listing becomes invalid)
    """


class TestGetAllProducts(unittest.TestCase):
    """Tests the behaviour of the function get_all_products

    What is tested
    --------------
    - return type is list
    """


class TestGetSearchPages(unittest.TestCase):
    """Tests the behaviour of the function get_search_pages

    What is tested
    --------------
    - return type is list
    - in returned pages there are products
    """


class TestMLQuery(unittest.TestCase):
    """Tests the behaviour of the function ML_query

    What is tested
    --------------
    - return type is list
    - returns correct reputation (consistent with is_reputable)
    - obeys order parameter
    """


if __name__ == "__main__":
    unittest.main()
