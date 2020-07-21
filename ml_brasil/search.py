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
    imported. Returns the products resulted from the search as a list
    to be handled by the application.
    """
    products = parse.get_all_products(parse.get_search_pages(search_term,
                                                             category,
                                                             price_min,
                                                             price_max,
                                                             condition,
                                                             aggressiveness),
                                      min_rep)
    return sorted(products, key=lambda p: p["price"], reverse=(order == 2))
