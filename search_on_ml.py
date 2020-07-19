import ml_brasil


def format_price(price):
    i = str(price[0])
    c = ("0" + str(price[1])) if price[1] < 10 else str(price[1])
    return f"R$ {i},{c}"


def print_product(product):
    print(f"""\
    Título: {product['title']}
    Preço: {format_price(product['price'])}
    Em promoção: {"Sim" if product['in-sale'] else "Não"}
    Frete grátis: {"Sim" if product['free-shipping'] else "Não"}
    Boa reputação: {"Sim" if product['reputable'] else "Não"}
    Sem Juros: {"Sim" if product['no-interest'] else "Não"}
    Link: {product['link']}
    Imagem: {product['picture']}""")


def print_cats():
    for father_cat in ml_brasil.parse.CATS:
        print(f"{father_cat[0][0]} ---> {father_cat[0][1]}:")
        print()
        for cat in father_cat[1]:
            print(f"{father_cat[0][0]}.{cat['number']} -> {cat['name']}")
        print()


def read_parameters():
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
        price_max = ml_brasil.parse.INT32_MAX
    if price_max < 0:
        raise ValueError("O preço máximo deve ser um valor positivo.")
    if price_max > ml_brasil.parse.INT32_MAX:
        raise ValueError(
            f"Valor muito grande: o preço máximo deve ser "
            f"um valor menor que {ml_brasil.parse.INT32_MAX}")

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

    while True:
        print("Qual é a condição desejada para os produtos?\n"
              "0 - ambos\n1 - novo\n2 - usado\n")
        try:
            condition = int(input())
            if condition in (0, 1, 2):
                break
        except ValueError:
            pass
        print("Você digitou um valor inválido.")

    try:
        aggressiveness = int(input(
            "Insira, entre 1 a 3 o nível desejado de agressividade:\n"
            "(Cuidado! Em um nível de agressividade alto, você pode ser"
            " bloqueado! "))
    except ValueError:
        aggressiveness = 2
    if aggressiveness not in (1, 2, 3):
        aggressiveness = 2

    return category, price_min, price_max, condition, aggressiveness


if __name__ == "__main__":
    while True:
        search_term = input("Digite os termos da pesquisa: ")
        advanced_mode = input(
            "Deseja utilizar as opções avançadas de pesquisa? "
            "Digite \"sim\" se positivo: ")
        if 'sim' in advanced_mode.lower():
            args = read_parameters()
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

        products = ml_brasil.ML_query(search_term, order, min_rep, *args)

        for product in products:
            if product["reputable"]:
                print_product(product)
                print()

        if input("Deseja encerrar ou fazer outra pesquisa? "
                 "Se quer fazer outra pesquisa, "
                 "digite \"sim\" sem aspas. ").lower().strip() in "sim":
            continue
        break
