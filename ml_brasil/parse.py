"""Request, extract and parse searches

This module contains functions that treat raw extracted searches'
content.
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
    def __init__(self, product_tag, process=True, check_rep=True, min_rep=3):
        self.html_tag = product_tag
        if process:
            self.processed = True
            self.link = get_link(product_tag)
            self.title = get_title(product_tag)
            self.price = get_price(product_tag)
            self.interest = is_no_interest(product_tag)
            self.free_shipping = has_free_shipping(product_tag)
            self.in_sale = is_in_sale(product_tag)
            self.picture = get_picture(product_tag)
            self.reputable = is_reputable(get_link(product_tag),
                                          min_rep) if check_rep else None
        else:
            self.processed = False


def get_link(product):
    """Extracts the link for the product tag

    As there are two types of listings in MercadoLivre (for products),
    the "catalogue" type listing and the "standard" type listing, the
    former ending with MLB112313123, and the latter ending with "-_JM",
    the procedure executed here is to extract the raw href from the pro-
    duct tag, which may contain irrelevant trailing information, and
    using a regular expression, matching only the relevant part, and
    returning that value which will be in the most compact and meaning-
    ful form.

    Parameters
    ----------
    product
        A product html tag extracted from the search pages.

    Returns
    -------
    str
        An url for the product listing on MercadoLivre if successful,
        an empty string otherwise.

    """
    LINK_CATCHER = compile(r"(https?://.+(?:MLB\d+\?|-_JM))")
    link = product.find(class_="item__info-title")
    if link:
        link = link.get("href").strip()
        link = search(LINK_CATCHER, link)
        link = link[0]
        link = link[:-1] if link[-1] == '?' else link
        return link
    return ""


def get_title(product):
    """Extracts the title from the product tag

    Parameters
    ----------
    product
        A product html tag extracted from the search pages.

    Returns
    -------
    str
        The title of the product listing on MercadoLivre, an empty
        string otherwise.

    """
    title_tag = product.find(class_="main-title")
    if not title_tag:
        title_tag = ""
    else:
        title_tag = title_tag.contents[0].strip()
    return title_tag


def get_price(product):
    """Extracts the price from the product tag

    Parameters
    ----------
    product
        A product html tag extracted from the search pages.

    Returns
    -------
    tuple
        If sucessful, returns the price of the product as a tuple, with
        the first element of the tuple being the integer part of the
        price, and the second being the fractional part. Otherwise, re-
        turns the tuple (float('nan'), float('nan')).

    """
    price_container = product.find(class_="price__container")
    if price_container:
        price_int = price_container.find(
            class_="price__fraction").contents[0].strip()
        price_int = int(float(price_int) * (1 if len(price_int) < 4 else 1000))
        price_cents = price_container.find(class_="price__decimals")
        price_cents = 0 if not price_cents else int(price_cents.contents[0].strip())
    else:
        price_int, price_cents = float('nan'), float('nan')
    return (price_int, price_cents)


def get_picture(product):
    """Extracts the link for the picture from the product tag

    Parameters
    ----------
    product
        A product html tag extracted from the search pages.

    Returns
    -------
    str
        An url for the product picture on MercadoLivre if successful,
        an empty string otherwise.

    """
    picture = ""
    image_tag = product.find(class_="item__image item__image--stack")
    if image_tag:
        picture = image_tag.find("img").get("src")
        if not picture:
            picture = image_tag.find("img").get("data-src")
        if not picture:
            picture = ""

    return picture


def is_no_interest(product):
    """Verifies wether the installments for payment have interest

    Parameters
    ----------
    product
        A product html tag extracted from the search pages.

    Returns
    -------
    bool
        True if the installments are interest-free, False otherwise.

    """
    return "item-installments free-interest" in str(product)


def has_free_shipping(product):
    """Verifies wether the shipping of the product is free of charge

    Parameters
    ----------
    product
        A product html tag extracted from the search pages.

    Returns
    -------
    bool
        True if the shipping is free, False otherwise.

    """
    return "stack_column_item shipping highlighted" in str(product)


def is_in_sale(product):
    """Verifies wether the product's current price is discounted

    Parameters
    ----------
    product
        A product html tag extracted from the search pages.

    Returns
    -------
    bool
        True if the current price is discounted from the full price,
        False otherwise.

    """
    return "item__discount" in str(product)


def is_reputable(link, min_rep=3, aggressiveness=2):
    """Verifies wether the seller's reputation is sufficient

    The way is_reputable checks if a listing is from a reputable seller
    is by requesting the product page from MercadoLivre, and checking
    the reputation level of the seller. If min_rep is zero, this doesn't
    need to be checked and the function can return True right away.

    In 'catalogue' type listings this is not possible, but MercadoLivre
    already filters most unreputable sellers from those listings, and
    therefore these type of listings can always be considered reputable.

    Parameters
    ----------
    link
        The url for the product listing
    min_rep
        The reputation level threshold that a seller has to reach for
        them to be considered reputable.
    aggressiveness
        The level of aggressiveness (speed) that the function will do
        html requests. The higher its value, the shorter the delay be-
        tween requests.

    Returns
    -------
    bool
        True if the listing has the minimum reputation required or is
        one of the exceptional cases, False otherwise.

    Note
    ----
    is_reputable is the main performance bottleneck of the package.
    It is called once for every product in a search, which can mean
    hundreds or up to a few thousands times. Almost every call makes an
    html request, and then waits for a number of milisseconds. This is
    necessary to avoid being ip blocked from MercadoLivre servers, but
    adds a huge bottleneck to the package. Any optimization on this
    function is very valuable.

    """
    if min_rep > 0:
        if not link:
            return False

        sleep(0.5**aggressiveness)
        product = BeautifulSoup(get(link).text, "html.parser")

        if "ui-pdp-other-sellers__title" not in str(product):
            thermometer = product.find(class_="card-section seller-thermometer")
            THERM_LEVELS = ("newbie", "red", "orange",
                            "yellow", "light_green", "green")[0:min_rep]
            if any(badrep in str(thermometer)
                   for badrep in THERM_LEVELS) or thermometer is None:
                return False

    return True


def get_cat(catid):
    """Fetches the category information from the database

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


def get_all_products(pages, min_rep):
    """Parses the pages to generate final results

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

    Returns
    -------
    list[dict]
        A list of which each element is a dict that represents a product
        and it's pertaining information.

    """
    products = [
        BeautifulSoup(page, "html.parser")
        .find_all(class_="results-item highlighted article stack product")
        for page in pages]

    return [{
            "link": get_link(product),
            "title": get_title(product),
            "price": get_price(product),
            "no-interest": is_no_interest(product),
            "free-shipping": has_free_shipping(product),
            "in-sale": is_in_sale(product),
            "reputable": is_reputable(
                get_link(product), min_rep),
            "picture": get_picture(product)}
            for page in products for product in page]


def get_search_pages(term, cat='0.0',
                     price_min=0, price_max=INT32_MAX,
                     condition=0, aggressiveness=2):
    """Searches in MercadoLivre with the specified arguments

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
