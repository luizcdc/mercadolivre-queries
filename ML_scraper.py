import bs4
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from pickle import load
from urllib.parse import quote

SKIP_PAGES = 1500  # 0 unless debugging
KEYS_PORTUGUESE = {'link': 'Link', 'title': 'Título', 'price': 'Preço', 'no-interest': 'Parcelamento sem Juros',
                   'in-sale': 'Em Promoção', 'reputable': 'Boa reputação', 'picture': 'Link da imagem', 'free-shipping': 'Frete Grátis'}
with open("categories.pickle", "rb") as cat:
    CATS = load(cat)


def get_link(product):
    link = product.find(class_="item__info-title").get("href").strip()
    jm_loc = link.find('-_JM')
    if jm_loc == -1:
        return link
    return link[:jm_loc + 4]


def get_title(product):
    return product.find(class_="main-title").contents[0].strip()


def get_price(product):
    price = product.find(
        class_="price__fraction").contents[0].strip()
    return float(price) * (1 if len(price) < 4 else 1000)


def get_picture(product):
    picture = product.find(class_="item__image item__image--stack").find("img").get("src")
    if not picture:
        picture = product.find(class_="item__image item__image--stack").find("img")["data-src"]
    return picture


def is_no_interest(product):
    return True if product.find(class_="stack_column_item installments highlighted").contents[0].get(
        "class") == "item-installments free-interest" else False


def has_free_shipping(product):
    return "stack_column_item shipping highlighted" in str(product)


def is_in_sale(product):
    return "item__discount" in str(product)


def get_all_products(pages, min_rep):
    products = [
        BeautifulSoup(
            page,
            "html.parser").find_all(
            class_="results-item highlighted article stack product") for page in pages]

    return [{
            "link": get_link(product),
            "title": get_title(product),
            "price": get_price(product),
            "no-interest": is_no_interest(product),
            "free-shipping": has_free_shipping(product),
            "in-sale": is_in_sale(product),
            "reputable": is_reputable(
                get_link(product), min_rep),
            "picture": get_picture(product)} for page in products for product in page]


def is_reputable(link, min_rep=3, aggressiveness=2):
    product_page = BeautifulSoup(get(link).text, "html.parser")
    thermometer = str(
        product_page.find(
            class_="card-section seller-thermometer"))
    sleep(0.5**aggressiveness)
    THERM_LEVELS = ("newbie", "red", "orange",
                    "yellow", "light_green", "green")
    if any(badrep in thermometer for badrep in (THERM_LEVELS[i] for i in range(min_rep))):
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
    for father_cat in CATS:
        if father_cat[0][0] == father_num:
            for child in father_cat[1]:
                if child['number'] == child_num:
                    subdomain = child['subdomain']
                    suffix = child['suffix']
                    break
    return subdomain, suffix


def get_search_pages(term, cat='0.0', price_min=0, price_max=2147483647, condition=0, aggressiveness=2):
    CONDITIONS = ["", "_ITEM*CONDITION_2230284", "_ITEM*CONDITION_2230581"]
    CATS.insert(0, [[0, 'Todas as categorias'], [
                {'subdomain': 'lista', 'suffix': '', 'number': 0, 'name': 'Todas'}]])
    subdomain, suffix = get_cat(cat)
    index = 1
    pages = []
    while True:
        page = get(
            f"https://{subdomain}.mercadolivre.com.br/{suffix}{quote(term, safe='')}_Desde_{index}_PriceRange_{price_min}-{price_max}{CONDITIONS[condition]}")
        index += 50 * (SKIP_PAGES + 1)  # DEBUG
        if page.status_code == 404:
            break
        else:
            pages.append(page.text)
        sleep(0.5**aggressiveness)
    return pages


def get_parameters():
    # TODO: ADD EXCEPTION HANDLING
    price_min = int(input(
        "Digite como um número inteiro, sem outros símbolos, o preço mínimo para os resultados da pesquisa (Ex: '150' sem aspas para R$ 150,00): "))
    price_max = int(input(
        "Digite como um número inteiro, sem outros símbolos, o preço máximo para os resultados da pesquisa (Ex: '1500' sem aspas para R$ 1500,00): "))
    if price_min > price_max:
        price_min, price_max = price_max, price_min
    condition = int(input(
        "Insira a condição do produto para os resultados da busca.\n(0 - misto | 1 - novo | 2 - usado): "))
    print_cats()
    category = input(
        "Insira a categoria de acordo com os código identificadores exibidos\n(Ex: Caso queira a categoria \"Adultos\", digite '31.1' sem aspas): ")

    aggressiveness = (int(input(
        "Insira, entre 1 a 3 o nível desejado de agressividade:\n(Cuidado! Em um nível de agressividade alto, você pode ser bloqueado! )")) % 4) - 1

    return category, price_min, price_max, condition, aggressiveness


def ML_query(search_term, order=1, min_rep=3, category='0.0', price_min=0, price_max=2147483647, condition=0, aggressiveness=2):
    products = get_all_products(get_search_pages(search_term, category,
                                                 price_min, price_max, condition, aggressiveness), min_rep)
    return sorted(products, key=lambda p: p["price"], reverse=order == 2)


if __name__ == "__main__":
    search_term = input("Digite os termos da pesquisa: ")
    advanced_mode = input(
        "Deseja utilizar as opções avançadas de pesquisa? Digite \"sim\" se positivo: ")
    if 'sim' in advanced_mode.lower():
        args = get_parameters()
        order = int(input(
            "Insira a ordenação desejada dos resultados.\n(0 - relevância | 1 - preço mínimo | 2 - preço máximo): "))
        min_rep = int(input(
            "Insira, entre 0 a 6, qual é o nível mínimo de reputação desejada para os vendedores: "))
    else:
        args = ()
        order = 1
        min_rep = 3
    products = ML_query(search_term, order, min_rep, *args)

    for product in products:
        if product["reputable"]:
            print_product(product)
            print()
    # TODO: ASK IF USER INTENDS TO DO ANOTHER SEARCH
