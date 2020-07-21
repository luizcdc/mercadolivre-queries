"""Request, extract and parse searches

This module contains functions that treat raw extracted searches'
content.
"""
import importlib.resources as resources
import bs4
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
    return "item-installments free-interest" in str(product)


def has_free_shipping(product):
    return "stack_column_item shipping highlighted" in str(product)


def is_in_sale(product):
    return "item__discount" in str(product)


def get_all_products(pages, min_rep):
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


def is_reputable(link, min_rep=3, aggressiveness=2):
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
                   for badrep in THERM_LEVELS) or thermometer == None:
                return False

    return True


def get_cat(catid):
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
