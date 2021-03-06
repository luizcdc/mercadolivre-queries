"""Request, extract and parse searches.

This module contains functions that process raw extracted searches'
contents and the Product class.
"""
import importlib.resources as resources
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from pickle import load
from urllib.parse import quote
from re import compile, search
from . import categories

SKIP_PAGES = 0  # 0 unless debugging
"""int: Sets how many pages will be skipped in a search

This variable is useful for debugging purposes inside the function
get_search_pages. When set to an integer value greater than zero, will
skip that number of pages. Greatly speeds a search if only executing the
search for testing purposes, due to the diminished number of pages from
which to extract information.

Example
-------
    If SKIP_PAGES == 15, get_search_pages will request page 1 of the
    search, and then proceed to request page 16, skipping pages 2-15.
    If successful, page 31 will be requested. This continues until the
    answer is code 404, and then get_search_pages returns.
"""

INT32_MAX = 2 ** 31 - 1
"""int: Maximum value that a 32-bit signed integer can have

Used as a maximum value constant respecting the engeneering constraints
of the MercadoLivre website.
"""

try:
    with resources.open_binary(categories, "categories.pickle") as cat:
        CATS = load(cat)
        """list: The categories database

        Please refer to the categories subpackage's documentation.
        """
except FileNotFoundError:
    raise FileNotFoundError("The categories.pickle database could not be "
                            "loaded. Try to generate a new updated data"
                            "base with the extract_categories script, or "
                            "to reinstall the module.")


class Product:
    """A product listing in MercadoLivre Brasil.

    All data about a product object can be inferred by its html tag and
    its product page, acessible through its url.

    """

    min_rep = 3
    """The minimum reputation for a seller to be reputable."""
    aggressiveness = 3
    """The speed with which html requests will be performed."""

    _THERMOMETER_LEVELS = ("newbie", "red",
                           "orange", "yellow",
                           "light_green", "green")
    """The 6 possible level for the reputation of a seller, in order."""

    def __init__(self, product_tag, process=True, check_rep=True):
        """Initialize Product with the html tag.

        Before initializing the first Product object, it is recommended
        to set the class variable 'min_rep' to the desired value for
        that particular search, to assure consistency between all pro-
        ducts. self._html_tag is always initialized with the bs4 html
        tag for the product. The initialization of other attributes can
        be delayed until the first time they are acessed. To do this,
        the arguments process and/or check_rep need to be set to False.

        Parameters
        ----------
        product_tag
            The bs4 html tag for the product.
        process
            Whether the values for the attributes of the product are to
            be obtained in initialization or later on.
        check_rep
            Whether the reputation of the seller is to be verified in
            initialization or later on.
        min_rep
            The reputation level threshold that a seller of the product
            has to reach for them to be considered reputable.

        """
        self._html_tag = product_tag
        if process:
            # accessing the attribute for the first time sets it
            self.link
            self.title
            self.price
            self.no_interest
            self.free_shipping
            self.in_sale
            self.picture
            if check_rep:
                self.reputable

    @property
    def link(self):
        """str: The link for the product listing.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts the link for the listing
        from self._html_tag.

        """
        if not hasattr(self, '_link'):
            self._link = self._extract_link()
        return self._link

    @property
    def title(self):
        """str: The title for the product listing.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts the title for the listing
        from self._html_tag.

        """
        if not hasattr(self, '_title'):
            self._title = self._extract_title()
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Type must be str")
        self._title = value

    @property
    def price(self):
        """tuple[int,int]: The price for the product listing.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts the price for the listing
        from self._html_tag.

        """
        if not hasattr(self, '_price'):
            self._price = self._extract_price()
        return self._price

    @property
    def no_interest(self):
        """bool: Whether payment in installments is interest free.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts the interest information
        from self._html_tag.

        """
        if not hasattr(self, '_no_interest'):
            self._no_interest = self._is_no_interest()
        return self._no_interest

    @property
    def free_shipping(self):
        """bool: Whether the shipping of the product is free of charge.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts the shipping information
        for the listing from self._html_tag.

        """
        if not hasattr(self, '_free_shipping'):
            self._free_shipping = self._has_free_shipping()
        return self._free_shipping

    @property
    def in_sale(self):
        """bool: Whether product's price is discounted at the moment.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts in self._html_tag the
        value for in_sale.

        """
        if not hasattr(self, '_in_sale'):
            self._in_sale = self._is_in_sale()
        return self._in_sale

    @property
    def picture(self):
        """str: The picture for the product listing.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts the picture for the lis-
        ting from self._html_tag.

        """
        if not hasattr(self, '_picture'):
            self._picture = self._extract_picture()
        return self._picture

    @property
    def reputable(self):
        """bool: Whether the product's seller is reputable.

        In case the property was not initialized in __init__, in the
        first time it is accessed, it extracts whether the seller is
        reputable by performing an html request for the listing page,
        which is a costly operation.

        """
        if not hasattr(self, '_reputable'):
            self._reputable = self._is_reputable()

        return self._reputable

    def _extract_link(self):
        """Extract the link for the product tag.

        As there are two types of listings in MercadoLivre (for products),
        the "catalogue" type listing and the "standard" type listing, the
        former ending with MLB112313123, and the latter ending with "-_JM",
        the procedure executed here is to extract the raw href from the pro-
        duct tag, which may contain irrelevant trailing information, and
        using a regular expression, matching only the relevant part, and
        returning that value which will be in the most compact and meaning-
        ful form.

        Returns
        -------
        str
            An url for the product listing on MercadoLivre if successful,
            an empty string otherwise.

        """
        LINK_CATCHER = compile(r"(https?://.+(?:MLB\d+\?|-_JM))")
        link = self._html_tag.find(class_="item__info-title")
        if link:
            link = link.get("href").strip()
            link = search(LINK_CATCHER, link)
            link = link[0]
            link = link[:-1] if link[-1] == '?' else link
            return link
        return ""

    def _extract_title(self):
        """Extract the title from the product tag.

        Returns
        -------
        str
            The title of the product listing on MercadoLivre, an empty
            string otherwise.

        """
        title_tag = self._html_tag.find(class_="main-title")
        if not title_tag:
            title_tag = ""
        else:
            title_tag = title_tag.contents[0].strip()
        return title_tag

    def _extract_price(self):
        """Extract the price from the product tag.

        Returns
        -------
        tuple
            If sucessful, returns the price of the product as a tuple, with
            the first element of the tuple being the integer part of the
            price, and the second being the fractional part. Otherwise, re-
            turns the tuple (float('nan'), float('nan')).

        """
        price_container = self._html_tag.find(class_="price__container")
        if price_container:
            price_int = price_container.find(
                class_="price__fraction").contents[0].strip()
            price_int = int(price_int.replace('.', ''))
            price_cents = price_container.find(class_="price__decimals")
            price_cents = 0 if not price_cents else int(price_cents
                                                        .contents[0].strip())
        else:
            price_int, price_cents = float('nan'), float('nan')
        return (price_int, price_cents)

    def _is_no_interest(self):
        """Verify wether the installments for payment have interest.

        Returns
        -------
        bool
            True if the installments are interest-free, False otherwise.

        """
        return "item-installments free-interest" in str(self._html_tag)

    def _has_free_shipping(self):
        """Verify wether the shipping of the product is free of charge.

        Returns
        -------
        bool
            True if the shipping is free, False otherwise.

        """
        return "stack_column_item shipping highlighted" in str(self._html_tag)

    def _is_in_sale(self):
        """Verify wether the product's current price is discounted.

        Returns
        -------
        bool
            True if the current price is discounted from the full price,
            False otherwise.

        """
        return "item__discount" in str(self._html_tag)

    def _extract_picture(self):
        """Extract the link for the picture from the product tag.

        Returns
        -------
        str
            An url for the product picture on MercadoLivre if success-
            ful, an empty string otherwise.

        """
        picture = ""
        img_tag = self._html_tag.find(class_="item__image item__image--stack")
        if img_tag:
            picture = img_tag.find("img").get("src")
            if not picture:
                picture = img_tag.find("img").get("data-src")
            if not picture:
                picture = ""

        return picture

    def _is_reputable(self):
        """Verify wether the seller's reputation is sufficient.

        The way is_reputable checks if a listing is from a reputable seller
        is by requesting the product page from MercadoLivre, and checking
        the reputation level of the seller. If min_rep is zero, this doesn't
        need to be checked and the function can return True right away.

        In 'catalogue' type listings this is not possible, but MercadoLivre
        already filters most unreputable sellers from those listings, and
        therefore these type of listings can always be considered reputable.


        Returns
        -------
        bool
            True if the listing has the minimum reputation required or is
            one of the exceptional cases, False otherwise.

        Note
        ----
        _is_reputable is the main performance bottleneck of the package.
        It is called once for every product in a search, which can mean
        hundreds or up to a few thousands times. Almost every call makes an
        html request, and then waits for a number of milisseconds. This is
        necessary to avoid being ip blocked from MercadoLivre servers, but
        adds a huge bottleneck to the package. Any optimization on this
        function is very valuable.

        """
        if self.min_rep > 0:
            if not self.link:
                return False

            sleep(0.5**self.aggressiveness)
            product_page = BeautifulSoup(get(self.link).text, "html.parser")

            if "ui-pdp-other-sellers__title" not in str(product_page):
                thermometer = (product_page
                               .find(class_="card-section seller-thermometer"))
                therm_levels = self._THERMOMETER_LEVELS[0:self.min_rep]
                if any(badrep in str(thermometer)
                       for badrep in therm_levels) or thermometer is None:
                    return False
        return True

    def _format_price(self):
        price = self.price
        i = str(price[0])
        c = ("0" + str(price[1])) if price[1] < 10 else str(price[1])
        return f"R$ {i},{c}"

    def __repr__(self):
        """Return string representation of the object.

        Returns a string which contains the attributes of the product in
        Brazilian Portuguese, in an human-readable format.
        """
        price = self._format_price()
        return (f"Título: {self.title}\n" +
                f"Preço: {price}" +
                " " * (23 - len(price)) +  # some math because price varies
                f"Frete grátis: {'Sim' if self.free_shipping else 'Não'}" +
                " " * 13 +
                f"Em promoção: {'Sim' if self.in_sale else 'Não'}\n" +
                f"Boa reputação: {'Sim' if self.reputable else 'Não'}" +
                " " * 12 +
                f"Sem Juros: {'Sim' if self.no_interest else 'Não'}\n" +
                f"Link: {self.link[8:]}\n" +  # doesn't print https://
                f"Imagem: {self.picture[8:]}")  # doesn't print https://


def get_cat(catid):
    """Fetch the category information from the database.

    Using the category id, fetches the information needed to perform
    searches, namely the subdomain and suffix for the search url. If
    the requested category does not exist, raises a ValueError.

    Parameters
    ----------
    catid
        A string in the format "X.Y" where X and Y are integers.

    Returns
    -------
    subdomain
        The subdomain of mercadolivre.com.br which is used for searches
        in the requested category.
    suffix
        The suffix for mercadolivre.com.br which is used for searches in
        the requested category.

    """
    father_num, child_num = map(int, catid.split('.'))
    subdomain = False
    for father_cat in CATS:
        if father_cat[0][0] == father_num:
            for child in father_cat[1]:
                if child['number'] == child_num:
                    subdomain = child['subdomain']
                    suffix = child['suffix']
                    break
    if not subdomain:
        raise ValueError(f"Categoria informada \"{catid}\" não existe.")

    return subdomain, suffix


def get_all_products(pages, min_rep=Product.min_rep, process=True):
    """Process the pages to generate final results.

    Goes through the pages in the list returned by get_search_pages ex-
    tracting each product from all the pages, and then extracting pro-
    duct information from each product.

    Parameters
    ----------
    pages
        A list of strings which contain raw html from the pages of the
        search results.
    min_rep
        The reputation level threshold that a seller has to reach for
        them to be considered reputable.
    process
        Whether all products returned will be processed completely be-
        fore returning the list of products.

    Returns
    -------
    list[Product]
        A list of which each element is a Product object.

    """
    Product.min_rep = min_rep
    products = [
        BeautifulSoup(page, "html.parser")
        .find_all(class_="results-item highlighted article stack product")
        for page in pages]
    return [Product(product_tag=product, process=process)
            for page in products for product in page]


def get_search_pages(term, cat='0.0',
                     price_min=0, price_max=INT32_MAX,
                     condition=0, aggressiveness=3):
    """Search in MercadoLivre with the specified arguments.

    This function does the requesting to MercadoLivre, returning every
    result page as raw html strings in a list. Does not return pages
    that contain no products.

    Parameters
    ----------
    term
        The search term. Trailing and leading spaces are stripped.
    cat
        The category number for the desired category for the products.
    price_min
        The minimum price of a listing for it to be included in the
        results. Always a non-negative integer, lower than price_max.
    price_max
        The maximum price of a listing for it to be included in the
        results. Always a non-negative integer, higher than price_min.
    condition
        Whether the product listings should to be new (1), used (2)
        or either (0).
    aggressiveness
        The level of aggressiveness (speed) that the function will do
        html requests. The higher its value, the shorter the delay be-
        tween requests.

    Returns
    -------
    list[str]
        A list of which each element is a raw html strings of the search
        result pages.

    """
    CONDITIONS = ["", "_ITEM*CONDITION_2230284", "_ITEM*CONDITION_2230581"]
    subdomain, suffix = get_cat(cat)
    index = 1
    pages = []
    while True:
        sleep(0.5**aggressiveness)
        page = get(
            f"https://{subdomain}.mercadolivre.com.br/{suffix}"
            f"{quote(term, safe='')}_Desde_{index}"
            f"_PriceRange_{price_min}-{price_max}{CONDITIONS[condition]}")
        index += 50 * (SKIP_PAGES + 1)  # DEBUG
        if page.status_code == 404:
            break
        else:
            pages.append(page.text)
    return pages
