from . import parse


def ML_query(search_term, order=1,
             min_rep=3, category='0.0',
             price_min=0, price_max=parse.INT32_MAX,
             condition=0, aggressiveness=2):
    products = parse.get_all_products(parse.get_search_pages(search_term, category,
                                                             price_min, price_max,
                                                             condition, aggressiveness),
                                      min_rep)
    return sorted(products, key=lambda p: p["price"], reverse=(order == 2))
