import bs4
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from pickle import load
from urllib.parse import quote
from re import compile, search

SKIP_PAGES = 1500  # 0 unless debugging
INT32_MAX = 2147483647
KEYS_PORTUGUESE = {'link': 'Link',
                   'title': 'Título',
                   'price': 'Preço',
                   'no-interest': 'Parcelamento sem Juros',
                   'in-sale': 'Em Promoção',
                   'reputable': 'Boa reputação',
                   'picture': 'Link da imagem',
                   'free-shipping': 'Frete Grátis'}
try:
    with open("categories.pickle", "rb") as cat:
        CATS = load(cat)
except FileNotFoundError:
    raise FileNotFoundError("The categories.pickle database could not be "
                            "loaded. Try to generate a new updated data"
                            "base with the extract_categories script, or "
                            "to reinstall the module.")


def get_link(product):
    LINK_CATCHER = compile(r"(https?://.+(?:MLB\d+|-_JM))")
    link = product.find(class_="item__info-title")
    if link:
        link = link.get("href").strip()
        link = search(LINK_CATCHER, link)
        return link[0]
    return ""


def get_title(product):
    return product.find(class_="main-title").contents[0].strip()


def get_price(product):
    price = product.find(
        class_="price__fraction").contents[0].strip()
    return float(price) * (1 if len(price) < 4 else 1000)


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
    class_ = (product.find(class_="stack_column_item installments highlighted")
              .contents[0].get("class"))
    return class_ == "item-installments free-interest"


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
    sleep(0.5**aggressiveness)
    product_page = BeautifulSoup(get(link).text, "html.parser")
    thermometer = str(
        product_page.find(class_="card-section seller-thermometer"))
    THERM_LEVELS = ("newbie", "red", "orange",
                    "yellow", "light_green", "green")[0:min_rep]
    if any(badrep in thermometer for badrep in THERM_LEVELS):
        return False

    return True


def print_product(product):
    print(f"""\
    Título: {product['title']}
    Preço: {product['price']}
    Em promoção: {"Sim" if product['in-sale'] else "Não"}
    Frete grátis: {"Sim" if product['free-shipping'] else "Não"}
    Boa reputação: {"Sim" if product['reputable'] else "Não"}
    Sem Juros: {"Sim" if product['no-interest'] else "Não"}
    Link: {product['link']}
    Imagem: {product['picture']}""")


def print_cats():
    for father_cat in CATS:
        print(f"{father_cat[0][0]} ---> {father_cat[0][1]}:")
        print()
        for cat in father_cat[1]:
            print(f"{father_cat[0][0]}.{cat['number']} -> {cat['name']}")
        print()


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


def get_parameters():
    try:
        price_min = int(input(
            "Digite como um número inteiro, sem outros símbolos, o preço mínimo"
            " para os resultados da pesquisa (Ex: '150' sem aspas para "
            "R$ 150,00): "))
    except ValueError:
        price_min = 0
    if price_min < 0:
        raise ValueError("O preço mínimo não pode ser um valor negativo.")

    try:
        price_max = int(input(
            "Digite como um número inteiro, sem outros símbolos, o preço máximo"
            " para os resultados da pesquisa (Ex: '1500' sem aspas para "
            "R$ 1500,00): "))
    except ValueError:
        price_max = INT32_MAX
    if price_max < 0:
        raise ValueError("O preço máximo deve ser um valor positivo.")
    if price_max > INT32_MAX:
        raise ValueError(
            f"Valor muito grande: o preço máximo deve ser "
            f"um valor menor que {INT32_MAX}")

    if price_min > price_max:
        price_min, price_max = price_max, price_min

    print_cats()
    category = input(
        "Insira a categoria de acordo com os código identificadores exibidos\n"
        "(Ex: Caso queira a categoria \"Adultos\", digite '31.1' sem aspas): ")
    try:
        map(int, category.split('.'))
    except ValueError:
        raise ValueError("A categoria foi digitada incorretamente.")
    if len(category.split('.')) != 2:
        raise ValueError("A categoria foi digitada incorretamente.")

    try:
        aggressiveness = int(input(
            "Insira, entre 1 a 3 o nível desejado de agressividade:\n"
            "(Cuidado! Em um nível de agressividade alto, você pode ser"
            " bloqueado! )"))
    except ValueError:
        aggressiveness = 2
    if aggressiveness not in (1, 2, 3):
        aggressiveness = 2

    return category, price_min, price_max, condition, aggressiveness


def ML_query(search_term, order=1,
             min_rep=3, category='0.0',
             price_min=0, price_max=INT32_MAX,
             condition=0, aggressiveness=2):
    products = get_all_products(get_search_pages(search_term, category,
                                                 price_min, price_max,
                                                 condition, aggressiveness),
                                min_rep)
    return sorted(products, key=lambda p: p["price"], reverse=(order == 2))


if __name__ == "__main__":
    while True:
        search_term = input("Digite os termos da pesquisa: ")
        advanced_mode = input(
            "Deseja utilizar as opções avançadas de pesquisa? "
            "Digite \"sim\" se positivo: ")
        if 'sim' in advanced_mode.lower():
            args = get_parameters()
            try:
                order = int(input(
                    "Insira a ordenação desejada dos resultados.\n"
                    "(0 - relevância | 1 - preço mínimo | 2 - preço máximo): "))
            except ValueError:
                order = 1
            try:
                min_rep = int(input(
                    "Insira, entre 0 a 6, qual é o nível mínimo "
                    "de reputação desejada para os vendedores: "))
            except ValueError:
                min_rep = 3
        else:
            args = ()
            order = 1
            min_rep = 3

        products = ML_query(search_term, order, min_rep, *args)

        for product in products:
            if product["reputable"]:
                print_product(product)
                print()

        if input("Deseja encerrar ou fazer outra pesquisa? "
                 "Se quer fazer outra pesquisa, "
                 "digite \"sim\" sem aspas. ").lower().strip() in "sim":
            continue
        break
