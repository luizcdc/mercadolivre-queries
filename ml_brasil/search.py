"""Functions to perform searches on MercadoLivre

This module is the search interface of the package. Through ML_query,
the user may request a search with only the search term, and optional
keyword arguments. The results come already processed, in their final
form.
"""

from . import parse


def ML_query(search_term, order=1,
             min_rep=3, category='0.0',
             price_min=0, price_max=parse.INT32_MAX,
             condition=0, aggressiveness=2):
    """Calls for the search and returns ordered results

    This function is the main interface of the package. ML_query is in-
    tended to be the only thing from the package that is needed to be
    imported.

    Parameters
    ----------
    search_term
        The search term. Trailing and leading spaces are stripped.
    order
        The order by which the results must be sorted. Lower price (1),
        higher price (2), or 'relevance' (0) - MercadoLivre's default.
    min_rep
        The reputation level threshold that a seller has to reach for
        them to be considered reputable.
    category
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
    list[dict]
        A list of which each element is a dict that represents a product
        and it's pertaining information, ordered as per the order argu-
        ment.

    """
    products = parse.get_all_products(parse.get_search_pages(search_term,
                                                             category,
                                                             price_min,
                                                             price_max,
                                                             condition,
                                                             aggressiveness),
                                      min_rep)
    if order:
        products = sorted(products,
                          key=lambda p: p["price"],
                          reverse=(order == 2))
    return products
