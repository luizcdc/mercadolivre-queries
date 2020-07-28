import unittest
from re import search, match, compile
from bs4 import BeautifulSoup
from random import choice, randint
from math import isnan
import sys

try:
    sys.path.append('..//')
    import ml_brasil
except ModuleNotFoundError:
    raise ModuleNotFoundError("Could not import ml_brasil package. Either "
                              "install the package on your local python "
                              "package directory, or install the package in "
                              "the directory exactly one level above this "
                              "folder.")

backup_CATS = ml_brasil.parse.CATS.copy()

product = """<li class="results-item highlighted article stack product "> <div class="rowItem item product-item highlighted item--stack new with-reviews to-item has-variations" id="MLB1543163640"><div class="item__image item__image--stack"> <div class="images-viewer" item-url="https://www.mercadolivre.com.br/iphone-11-128-gb-preto-4-gb-ram/p/MLB15149567?source=search#searchVariation=MLB15149567&amp;position=1&amp;type=product&amp;tracking_id=b008d681-98e3-4479-90c6-98bd291f30f6" item-id="MLB1543163640" product-id="MLB15149567"> <div class="image-content"> <a href="https://www.mercadolivre.com.br/iphone-11-128-gb-preto-4-gb-ram/p/MLB15149567?source=search#searchVariation=MLB15149567&amp;position=1&amp;type=product&amp;tracking_id=b008d681-98e3-4479-90c6-98bd291f30f6" class="figure item-image item__js-link"> <img class="lazy-load" width="160" height="160" alt="iPhone 11 128 GB Preto 4 GB RAM" src="https://http2.mlstatic.com/D_NQ_NP_678481-MLA42453875909_072020-V.webp"> </a> </div> </div></div><div class="item__info-container highlighted "> <div class="item__info item--show-right-col "> <div class="item__highlight__container"> <div class="item__highlight item__highlight--deal" style="color: rgb(255, 255, 255); background: rgb(52, 131, 250); --darkreader-inline-color:#e8e6e3; --darkreader-inline-bgimage: initial; --darkreader-inline-bgcolor:#0447ac;" data-darkreader-inline-color="" data-darkreader-inline-bgimage="" data-darkreader-inline-bgcolor=""> Enviando normalmente </div> </div><h2 class="item__title list-view-item-title"> <a href="https://www.mercadolivre.com.br/iphone-11-128-gb-preto-4-gb-ram/p/MLB15149567?source=search#searchVariation=MLB15149567&amp;position=1&amp;type=product&amp;tracking_id=b008d681-98e3-4479-90c6-98bd291f30f6" class="item__info-title"> <span class="main-title"> iPhone 11 128 GB Preto 4 GB RAM </span> </a> <div class="item__brand"> <a class="item__brand-link" href="https://loja.mercadolivre.com.br/fast-shop"> <span class="item__brand-title-tos"> por Fast Shop </span> </a> </div></h2> <div class="price__container"> <span class="price-old" itemprop="price-old"> <del> R$&nbsp;6.099 </del> </span><div class="item__price item__price-discount"> <span class="price__symbol">R$</span> <span class="price__fraction">4.629</span></div> <div class="item__discount ">24% OFF</div> </div> <div class="item__stack_column highlighted"> <div class="item__stack_column__info"> <div class="stack_column_item installments highlighted"><span class="item-installments free-interest"> <span class="item-installments-multiplier"> 12x </span> <span class="item-installments-price"> R$ 385 <sup class="installment__decimals">75</sup> </span> <span class="item-installments-interest"> sem juros </span></span> </div> <div class="stack_column_item status"> <div class="item__status"> <div class="item__condition"> </div> </div> </div> </div> </div> <div class="stack_colum_right without-attributes with-reviews"> <div class="item__reviews"> <div class="stars"> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> <div class="star star-icon-full"></div> </div> <div class="item__reviews-total">232</div></div> <div class="stack_column_right__bottom item__has-variations"> <div class="variation-picker__container"> <div class="ui-dropdown custom"> <input type="checkbox" id="dropdown-variations-0" class="dropdown-trigger variation-picker__trigger" autocomplete="off" hidden="" data-id="MLB1543163640"> <label for="dropdown-variations-0" class="ui-dropdown__link"> <span class="variation-picker__label">Cor: </span> <span class="ui-dropdown__display variation-picker__label variation-picker__label-bold">Preto</span> <div class="ui-dropdown__indicator"></div> </label> <div class="ui-dropdown__content dropdown__variations-content variation-picker cursor-wait variation-picker__size-3" data-size="3"> <ul class=""> <li id="MLB15149567" class="attrBox skeleton__box--0 selected-option"> <img class="variation-picker__img" title="Preto" width="36" height="36" src="https://http2.mlstatic.com/D_Q_NP_857283-MLA42453875910_072020-S.webp"></li> <li id="MLB15149572" class="attrBox skeleton__box--3 "> <img class="variation-picker__img" title="(Product)Red" width="36" height="36" src="https://http2.mlstatic.com/D_Q_NP_608338-MLA42453875933_072020-S.webp"></li> <li id="MLB15149568" class="attrBox skeleton__box--5 "> <img class="variation-picker__img" title="Branco" width="36" height="36" src="https://http2.mlstatic.com/D_Q_NP_899930-MLA42453930760_072020-S.webp"></li></ul> </div> </div> </div> </div> </div> </div></div> <form class="item__bookmark-form" action="/search/bookmarks/MLB1543163640/make" method="post" id="bookmarkForm"> <button type="submit" class="bookmarks favorite " data-id="MLB1543163640"> <div class="item__bookmark"> <div class="icon"></div> </div> </button> <input type="hidden" name="method" value="add"> <input type="hidden" name="itemId" value="MLB1543163640"> <input type="hidden" name="_csrf" value="cbe9313a-32d9-4618-bc3d-c0bb7091ebce"> </form> </div></li>"""
# this raw html was extracted from a listing of the iPhone 11. It was chosen
# because usually an iPhone stays being commercialized for many years after its
# launch, meaning that is less likely that the link will break in the next 5
# years
PRODUCT_TAG = BeautifulSoup(product, "html.parser")
PRODUCT_OBJECT = ml_brasil.parse.Product(PRODUCT_TAG, process=False)
INCORRECT_TAG = BeautifulSoup("<span class=\"price__symbol\">R$</span>",
                              "html.parser")
INCORRECT_OBJECT = ml_brasil.parse.Product(INCORRECT_TAG, process=False)
URL_RE = compile(r"https?://(.+\.)?.+\..+")


class TestCategories(unittest.TestCase):
    """Test the integrity of the categories database.

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
        if self.last_test_altered_cats:
            self.cats = backup_CATS.copy()
        self.last_test_altered_cats = False

    def test_todas_inserted_in_0(self):
        """cats[0] must be "All Categories" ("Todas")."""
        self.assertTrue("todas" in self.cats[0][0][1].lower())
        self.assertEqual(self.cats[0][0][0], 0)
        self.__class__.last_test_altered_cats = False

    def test_all_unique_and_ordered(self):
        """Test for uniqueness and order of categories' X.Y IDs.

        All parent categories' numbers must be unique, and inside the
        list of children of a parent category, every element must have
        a unique number as well. They should be in crescent order.

        self.cats[0] doesn't need to pass this test because it is hardcoded,
        has only one child and it gets tested in test_todas_inserted_in_0
        anyway.
        """
        for former_parent, curr_parent in zip(self.cats, self.cats[1:]):
            self.assertEqual(former_parent[0][0] + 1, curr_parent[0][0])
            for former_child, curr_child in zip(curr_parent[1],
                                                curr_parent[1][1:]):
                self.assertEqual(former_child['number'] + 1,
                                 curr_child['number'])
        self.__class__.last_test_altered_cats = False

    def test_children_start_with_one(self):
        """Test if the 1st element of each parent category is number 1.

        The number here referred is child['number']. Together with
        all_unique_and_ordered() and todas_inserted_in_0(), this test
        is the final assurance that the categories database is ordered
        and unique, always starting from the number 1 (except in
        category 'Todas').
        """
        for curr_parent in self.cats[1:]:
            self.assertEqual(curr_parent[1][0]['number'], 1)

    def test_consistent_with_types(self):
        """Test randomly some categories for type consistency.

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
    """Test the behaviour of the function get_cat.

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
        """Return data from a random valid category."""
        parent = choice(ml_brasil.parse.CATS)
        child = choice(parent[1])
        return (f"{parent[0][0]}.{child['number']}",
                child["subdomain"], child["suffix"])

    def test_expected_outputs(self):
        """Test if given category is retrieved consistently."""
        for _ in range(10):
            cat_code, subdomain, suffix = TestGetCat.random_valid_category()
            ret_subdomain, ret_suffix = ml_brasil.parse.get_cat(cat_code)
            self.assertEqual(ret_subdomain, subdomain)
            self.assertEqual(ret_suffix, suffix)

    def test_returns_correct_types(self):
        """Test if get_cat returns a tuple of strings.

        Randomly chooses categories from CATS database, and checks if
        get_cat returns always two strings.
        """
        for _ in range(10):
            cat_code, _, _ = TestGetCat.random_valid_category()
            subdomain, suffix = ml_brasil.parse.get_cat(cat_code)
            self.assertTrue(isinstance(subdomain, str))
            self.assertTrue(isinstance(suffix, str))

    def test_subdomain_not_empty(self):
        """Asserts that the subdomain returned is never empty."""
        for _ in range(10):
            cat_code, _, _ = TestGetCat.random_valid_category()
            subdomain, _ = ml_brasil.parse.get_cat(cat_code)
            self.assertTrue(subdomain != "")

    def test_raises_ValueError_if_not_existent(self):
        """Asserts that non-existent input category raises a ValueError.

        This design choice, instead of defaulting for the "Todas" (all)
        category was deemed better because it signals when something is
        not working better than just ignoring it and performing a valid
        search despite not being able to input the right category.
        """
        for _ in range(10):
            with self.assertRaises(ValueError):
                (ml_brasil.parse.
                 get_cat(f"{randint(50,10000)}.{randint(50,10000)}"))

    def test_doesnt_modify_CATS(self):
        """Test that get_cat does not modify the content of CATS."""
        for _ in range(10):
            cat_code, _, _ = TestGetCat.random_valid_category()
            ml_brasil.parse.get_cat(cat_code)

        self.assertEqual(ml_brasil.parse.CATS, backup_CATS)


class TestExtractLink(unittest.TestCase):
    """Test the behaviour of the Product method _extract_link.

    What is tested
    --------------
    - return type is str
    - ._extract_link strips irrelevant information
    - ._extract_link doesn't return something that wasn't contained
    in the tag
    - ._extract_link returns an empty string if something went wrong
    - ._extract_link returns an url

    Details
    -------
    The 'stripping' test relies on the fact that, at the time of rele-
    ase of the first version of this program, every valid MercadoLivre
    product page link in its minimal version ends with "MLB1231231232"
    or "-_JM" (1231231232 standing for any arbitrary number).

    """

    def test_returns_string(self):
        """Test that the return type is str."""
        self.assertTrue(isinstance(PRODUCT_OBJECT._extract_link(), str))

    def test_link_is_from_tag(self):
        """Test that the final link is in the tag's text."""
        self.assertTrue(PRODUCT_OBJECT._extract_link() in product)

    def test_link_stripped_correctly(self):
        """Test if link was stripped of trailing irrelevant information.

        With re.search, match in link either MLB123123132 or -_JM, and
        these need to be the end of the link (123123132 stands for any
        arbitrary number).
        """
        self.assertTrue(search(r"MLB\d+$|-_JM$|^$",
                               PRODUCT_OBJECT._extract_link()))
        # TODO: needs another example product to test -_JM type links

    def test_failure_returns_empty_string(self):
        """Test the return in case of failure.

        The failure of this method, characterized by the extraction of
        a link that's not correctly ended, must return an empty string,
        which allows for the methods that rely on it to handle it
        accordingly.

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns an
        empty string, but simply when an incorrect/corrupted/different
        tag from the format this method was made too work with is pas-
        sed as an argument to Product's __init__, an empty string is
        returned.

        """
        self.assertEqual(INCORRECT_OBJECT._extract_link(), "")

    def test_returns_url(self):
        """Test if the returned value is an http/https url."""
        link_url = PRODUCT_OBJECT._extract_link()
        self.assertTrue(match(URL_RE, link_url) or link_url == "")


class TestExtractTitle(unittest.TestCase):
    """Test the behaviour of the Product method _extract_title.

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

    def test_string_stripped(self):
        """Test if the title is correctly stripped of spaces."""
        title = PRODUCT_OBJECT._extract_title()
        self.assertTrue(title.strip() == title)

    def test_extract_title_from_example(self):
        """Test if the title was correctly extracted from the example."""
        title = PRODUCT_OBJECT._extract_title()
        self.assertEqual(title, "iPhone 11 128 GB Preto 4 GB RAM")

    def test_empty_string_on_failure(self):
        """Test that _extract_title returns empty string when it fails.

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns an
        empty string, but simply when an incorrect/corrupted/different
        tag from the format this method was made too work with is pas-
        sed as an argument to Product's __init__, an empty string is
        returned.

        """
        self.assertEqual(INCORRECT_OBJECT._extract_title(), "")


class TestExtractPrice(unittest.TestCase):
    """Test the behaviour of the Product method _extract_price.

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

    def test_type_correct(self):
        """Test if returns the correct type for the example product."""
        price = PRODUCT_OBJECT._extract_price()
        self.assertTrue(isinstance(price, tuple) and
                        isinstance(price[0], int) and
                        isinstance(price[1], int))

    def test_get_price_from_example(self):
        """Test if the price was correctly extracted from the example."""
        self.assertEqual(PRODUCT_OBJECT._extract_price(), (4629, 0))

    def test_returns_correctly_on_failure(self):
        """Test that the return value on failure is (nan,nan).

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns an
        empty string, but simply when an incorrect/corrupted/different
        tag from the format this method was made too work with is pas-
        sed as an argument to Product's __init__, an empty string is
        returned.
        """
        price = INCORRECT_OBJECT._extract_price()
        self.assertTrue(isnan(price[0]), isnan(price[1]))


class TestGetPicture(unittest.TestCase):
    """Test the behaviour of the Product method _extract_picture.

    A picture is stored as a url (str). Failure to retrieve a picture of
    a product is not a fatal failure, and an empty string should be re-
    turned in case of failure.

    What is tested
    --------------
    - type is string
    - returned value is a url
    - returns empty string on failure
    - returns correctly for provided example

    """

    def test_return_type_is_string(self):
        """Test that the return type is a string."""
        self.assertTrue(isinstance(PRODUCT_OBJECT._extract_picture(), str))
        self.assertTrue(isinstance(INCORRECT_OBJECT._extract_picture(), str))

    def test_returned_value_is_url(self):
        """Test if the returned value is an http/https url."""
        picture_url = PRODUCT_OBJECT._extract_picture()
        self.assertTrue(match(URL_RE, picture_url) or picture_url == "")

    def test_failure_returns_empty_string(self):
        """Test if returns an empty string on failure.

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns an
        empty string, but simply when an incorrect/corrupted/different
        tag from the format this method was made too work with is pas-
        sed as an argument to Product's __init__, an empty string is
        returned.

        """
        self.assertEqual(INCORRECT_OBJECT._extract_picture(), "")

    def test_extract_picture_from_example(self):
        """Test if the picture was correctly extracted from the example."""
        self.assertEqual(PRODUCT_OBJECT._extract_picture(),
                         "https://http2.mlstatic.com/D_NQ_NP_"
                         "678481-MLA42453875909_072020-V.webp")


class TestIsNoInterest(unittest.TestCase):
    """Test the behaviour of the Product method is_no_interest.

    What is tested
    --------------
    - return type is bool
    - in failure returns false
    - returns correctly for provided example

    """

    def test_return_type_is_bool(self):
        """Test that the returned value is a bool."""
        self.assertTrue(isinstance(PRODUCT_OBJECT._is_no_interest(),
                                   bool))
        self.assertTrue(isinstance(INCORRECT_OBJECT._is_no_interest(),
                                   bool))

    def test_failure_returns_false(self):
        """Test if returns False on failure.

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns False,
        but simply when an incorrect/corrupted/different tag from the
        format this method was made too work with is passed as an argu-
        ment to Product's __init__, False boolean value is returned.

        """
        self.assertEqual(INCORRECT_OBJECT._is_no_interest(), False)

    def test_returns_correctly_for_examples(self):
        """Test if the result is consistent with the examples."""
        self.assertEqual(PRODUCT_OBJECT._is_no_interest(), True)


class TestHasFreeShipping(unittest.TestCase):
    """Test the behaviour of the Product method _has_free_shipping.

    What is tested
    --------------
    - return type is bool
    - failure returns false
    - returns correctly for provided example

    """

    def test_return_type_is_bool(self):
        """Test that the returned value is a bool."""
        self.assertTrue(isinstance(PRODUCT_OBJECT._has_free_shipping(),
                                   bool))
        self.assertTrue(isinstance(INCORRECT_OBJECT._has_free_shipping(),
                                   bool))

    def test_failure_returns_false(self):
        """Test if returns False on failure.

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns False,
        but simply when an incorrect/corrupted/different tag from the
        format this method was made too work with is passed as an argu-
        ment to Product's __init__, False boolean value is returned.

        """
        self.assertEqual(INCORRECT_OBJECT._has_free_shipping(), False)

    def test_returns_correctly_for_examples(self):
        """Test if the result is consistent with the examples."""
        self.assertEqual(PRODUCT_OBJECT._has_free_shipping(), False)


class TestIsInSale(unittest.TestCase):
    """Test the behaviour of the Product method _is_in_sale.

    What is tested
    --------------
    - return type is bool
    - failure returns false
    - returns correctly for provided example

    """

    def test_return_type_is_bool(self):
        """Test that the returned value is a bool."""
        self.assertTrue(isinstance(PRODUCT_OBJECT._is_in_sale(), bool))

    def test_failure_returns_false(self):
        """Test if returns False on failure.

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns False,
        but simply when an incorrect/corrupted/different tag from the
        format this method was made too work with is passed as an argu-
        ment to Product's __init__, False boolean value is returned.
        """
        self.assertEqual(INCORRECT_OBJECT._is_in_sale(), False)

    def test_returns_correctly_for_examples(self):
        """Test if the result is consistent with the examples."""
        self.assertEqual(PRODUCT_OBJECT._is_in_sale(), True)


class TestIsReputable(unittest.TestCase):
    """Test the behaviour of the Product method _is_reputable.

    What is tested
    --------------
    - return type is bool
    - failure returns false
    - returns correctly for provided example (may break if provided
    example of listing becomes invalid)

    """
    default_min_rep = ml_brasil.parse.Product.min_rep

    def setUp(self):
        ml_brasil.parse.Product.min_rep = self.default_min_rep

    def test_return_type_is_bool(self):
        """Test that the returned value is a bool."""
        self.assertTrue(isinstance(PRODUCT_OBJECT._is_reputable(), bool))

    def test_failure_returns_correctly(self):
        """Test if returns correct default value on failure.

        This test should not test whether if when the Product was ini-
        tialized with arguments of the incorrect type it returns any-
        thing, but simply when an incorrect/corrupted/different tag from
        the format this method was made too work with is passed as an
        argument to Product's __init__, a boolean value is returned on
        the terms that follow:

        It should return False for any min_rep above 0. If the min_rep
        passed as a parameter is 0, it should return True.

        """
        PRODUCT_OBJECT._link = ("https://www.mercadolivre.com.br/"
                                "link_invalido_deve_dar_404")
        # manually changes the _link value for PRODUCT_OBJECT,
        # needs to be undone in the end of this method.

        ml_brasil.parse.Product.min_rep = 0
        self.assertEqual(INCORRECT_OBJECT._is_reputable(), True)
        self.assertEqual(PRODUCT_OBJECT._is_reputable(), True)
        for rep in range(1, 6):
            ml_brasil.parse.Product.min_rep = rep
            self.assertEqual(INCORRECT_OBJECT._is_reputable(), False)
            self.assertEqual(PRODUCT_OBJECT._is_reputable(), False)

        delattr(PRODUCT_OBJECT, "_link")

    def test_returns_correctly_for_examples(self):
        """Test if the result is consistent with the examples."""
        for rep in range(6):
            ml_brasil.parse.Product.min_rep = rep
            self.assertEqual(PRODUCT_OBJECT._is_reputable(), True)
            # every iteration in this loop should return True
            # because the example provided is of a listing which
            # aggregates many sellers of a product onto a single
            # page, which impossibilitates the algorith to extract
            # the reputation of the seller, but in most of the cases
            # MercadoLivre already makes sure that in such listings
            # only reputable sellers are displayed. Because of that,
            # we can safely assume that the listing is reputable.

        # needs another example product to test actual identification of
        # reputation, specially with min_rep parameter. The issue is that
        # regular listings on mercadolivre are short-lived, so the test
        # would break fairly frequently.


class TestGetSearchPages(unittest.TestCase):
    """Test the behaviour of the function get_search_pages

    What is tested
    --------------
    - return type is list
    - in returned pages there are products
    - lenght of valid search is greater than 0
    - lenght of invalid search is 0
    """
    @classmethod
    def setUpClass(cls):
        """Builds the data which will be used by the TestCase

        This setUpClass sets the parse.SKIP_PAGES variable to a value
        that will make the queries made only fetch one page. This is do-
        ne with the intention that the queries take less time.

        Two queries which are going to be used by the tests are also
        performed, one with a very common keyword ("4 GB"), one with a
        random, arbitrary string, which should not return any result.
        """
        ml_brasil.parse.SKIP_PAGES = ml_brasil.parse.INT32_MAX
        # makes the returned query at most 1 page long, at least 0
        cls.query_1 = ml_brasil.parse.get_search_pages("4 GB")
        # a very common search term, guaranteed to return lots of results
        cls.query_2_zero_results = (ml_brasil.parse.
                                    get_search_pages("daD2sdOM134123daa123jhs"))

    def test_return_type_is_list(self):
        """Test that the returned value is a list"""
        self.assertTrue(isinstance(self.query_1, list))
        self.assertTrue(isinstance(self.query_2_zero_results, list))

    def test_has_products_in_page(self):
        """Assures that there are products in all pages returned

        This test will work for a valid or an empty search, but there
        is no need to test this for a empty search.
        """
        self.assertTrue(
            "results-item highlighted article stack product"
            in page for page in self.query_1)

    def test_lenght_greater_than_0_for_valid_search(self):
        """Test if a valid search returns at least one page"""
        self.assertTrue(self.query_1)

    def test_lenght_0_for_invalid_search(self):
        """Test if an empty search returns an empty list

        This test should not test whether if when the arguments are of
        incorrect types it returns [], but simply that when a search
        finds no products because of uncommon keywords, no pages are re-
        turned, but instead an empty list.
        """
        self.assertEqual(self.query_2_zero_results, [])

    @classmethod
    def tearDownClass(cls):
        """Resets the external variables used by the TestCase"""
        ml_brasil.parse.SKIP_PAGES = 0


class TestGetAllProducts(unittest.TestCase):
    """Test the behaviour of the function get_all_products

    What is tested
    --------------
    - return type is list of dict
    - if empty "pages" is passed, returns list of lenght 0
    """

    @classmethod
    def setUpClass(cls):
        """Builds the data which will be used by the TestCase

        This setUpClass sets the parse.SKIP_PAGES variable to a value
        that will make the queries made only fetch one page. This is do-
        ne with the intention that the queries take less time.

        A search that is going to be used by the tests is also performed
        with a very common keyword ("4 GB"). This query and an empty
        list are then passed as arguments to get_all_products (two dis-
        tinct calls), and the returned values are then used by the tests.
        """
        ml_brasil.parse.SKIP_PAGES = ml_brasil.parse.INT32_MAX
        # makes the returned query at most 1 page long, at least 0
        cls.valid_query = ml_brasil.parse.get_search_pages("4 GB")
        cls.products = get_all_products(self.valid_query)
        cls.products_from_empty = get_all_products([])

    def test_return_type_is_list_of_dict(self):
        """Assures the returned value is a list with only dict elements"""
        self.assertTrue(isinstance(self.products, list))
        for product in self.products:
            self.assertTrue(isinstance(product, dict))

    def test_returns_lenght_0_for_invalid_pages(self):
        """Test if an empty search returns an empty list

        This test should not test whether if when the arguments are of
        incorrect types it returns an empty list, but instead that, if
        an empty list is passed as argument, this is the behaviour.
        """
        self.assertEqual(self.products_from_empty, [])

    @classmethod
    def tearDownClass(cls):
        """Resets the external variables used by the TestCase"""
        ml_brasil.parse.SKIP_PAGES = 0
        # restores SKIP_PAGES to its original value


class TestMLQuery(unittest.TestCase):
    """Test the behaviour of the function ML_query

    This TestCase takes a long while to run...

    What is tested
    --------------
    - return type is list
    - obeys min_rep parameter (consistent with is_reputable)
    - obeys order parameter
    - obeys price_min/price_max parameters
    - raises ValueError if search_term is too short (minimum lenght 2)
    - failed search returns empty list
    """

    @classmethod
    def setUpClass(cls):
        """Builds the data which will be used by the TestCase

        A long, complete search is necessary for more thorough testing,
        but takes a lot of time, and for this reason, aggressiveness is
        set to the highest in all searches performed. Other searches are
        performed limiting their results to only the first page, to save
        time.
        """
        cls.REP_FOR_TEST = 4
        ml_brasil.parse.SKIP_PAGES = ml_brasil.parse.INT32_MAX
        cls.search_4gb_mul = ml_brasil.ML_query("4 GB",
                                                aggressiveness=3,
                                                order=1)

        # all searches below are at max 1 page long
        cls.search_4gb_sing = ml_brasil.ML_query("4 GB",
                                                 aggressiveness=3,
                                                 order=1,
                                                 price_min=500,
                                                 price_max=1500)
        cls.search_racao_sing = ml_brasil.ML_query("Ração",
                                                   aggressiveness=3,
                                                   min_rep=cls.REP_FOR_TEST,
                                                   order=2)
        cls.search_empty = ml_brasil.ML_query("asdasdsaq12ads23121asdddsa")
        cls.all_searches = (cls.search_4gb_mul, cls.search_4gb_sing,
                            cls.search_empty, cls.search_racao_sing)

        # the two tuples below are a classification done to more easily
        # test the correctness of the ordering of the search results.
        # when adding another search to testing, this must be updated
        cls.order_1 = (cls.search_4gb_mul, cls.search_4gb_sing)
        cls.order_2 = (cls.search_racao_sing,)

        ml_brasil.parse.SKIP_PAGES = 0

    def test_return_type_is_list(self):
        """Assures the returned value is a list with only dict elements"""
        for search in self.all_searches:
            self.assertTrue(isinstance(search, list))
            for product in search:
                self.assertTrue(isinstance(product, dict))

    def test_obeys_min_rep(self):
        """Test if the reputation for the items are correct"""
        for product in self.search_racao_sing:
            self.assertEqual(product["reputable"],
                             ml_brasil.parse.
                             is_reputable(product['link'],
                                          min_rep=self.REP_FOR_TEST,
                                          aggressiveness=3))

    def test_obeys_order(self):
        """Test if the search returned is correctly ordered

        To make the code in this test simpler, in setUpClass two tuples
        are defined which group together the searches done in setUpClas
        by which order the products should be sorted by as per the argu-
        ment passed to ML_query.
        """
        for search in self.order_1:
            iter1, iter2 = iter(search), iter(search)
            next(iter2)
            not_in_order = False
            for i1, i2 in zip(iter1, iter2):
                if i1['price'] > i2['price']:
                    not_in_order = True
                    break
            self.assertFalse(not_in_order)

        for search in self.order_2:
            iter1, iter2 = iter(search), iter(search)
            next(iter2)
            not_in_order = False
            for i1, i2 in zip(iter1, iter2):
                if i1['price'] < i2['price']:
                    not_in_order = True
                    break
            self.assertFalse(not_in_order)

    def test_obeys_price_brackets(self):
        """Test if the price_min price_max arguments are obeyed

        If it can be assumed that the products are ordered (which is
        tested in test_obeys_order), it's only necessary to check for
        the first and last product listings returned in the search.
        """
        # assuming it's ordered, just check first and last
        first, last = cls.search_4gb_sing[0], cls.search_4gb_sing[-1]
        self.assertTrue(first['price'] >= (500, 0))
        self.assertTrue(last['price'] <= (1500, 0))

    def test_returns_empty_list_if_too_short_search_term(self):
        """Test if a search term too short always returns an empty list"""
        self.assertEqual(ML_scraper.ML_query("    a  "), [])
        self.assertEqual(ML_scraper.ML_query("c"), [])

    def test_failure_returns_empty_list(self):
        """Test if an empty search returns an empty list

        This test should not test whether if when the arguments are of
        incorrect types it returns an empty list, but instead that, if
        no matching products were found in a search, the return value is
        an empty list.
        """
        self.assertEqual(self.search_empty, [])


if __name__ == "__main__":
    unittest.main()
