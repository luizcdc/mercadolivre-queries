import ml_brasil


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
    print()
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
    print()

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
    print()

    while True:
        print("Escolha entre 0 - ambos, 1 - novo, 2 - usado, a condição "
              "desejada para os produtos: ")
        try:
            condition = int(input())
            if condition in (0, 1, 2):
                break
        except ValueError:
            pass
        print("Você digitou um valor inválido.")
    print()

    try:
        aggressiveness = int(input(
            "Cuidado! Em um nível de agressividade alto, você pode ser "
            "bloqueado!\n"
            "Insira, entre 1 a 3 o nível desejado de agressividade: "))
    except ValueError:
        aggressiveness = 3
    if aggressiveness not in (1, 2, 3):
        aggressiveness = 3
    print()

    return category, price_min, price_max, condition, aggressiveness


if __name__ == "__main__":
    while True:
        search_term = input("Digite os termos da pesquisa: ")
        advanced_mode = input(
            "Deseja utilizar as opções avançadas de pesquisa? "
            "Digite 'sim' se positivo, ou qualquer outra coisa para ignorar: ")
        if 'sim' in advanced_mode.lower():
            args = read_parameters()
            try:
                order = int(input(
                    "Dentre as opções "
                    "0 - relevância, 1 - preço mínimo, 2 - preço máximo, "
                    " insira a ordenação desejada dos resultados: "))
            except ValueError:
                order = 1
            print()
            try:
                min_rep = int(input(
                    "Insira, entre 0 a 6, qual é o nível mínimo "
                    "de reputação desejada para os vendedores: "))
            except ValueError:
                min_rep = 3
            print()
            print()
        else:
            args = ()
            order = 1
            min_rep = 3

        products = ml_brasil.ML_query(search_term, order,
                                      min_rep, *args, process=False)
        print("RESULTADOS:\n")
        for product in products:
            if product.reputable:
                print(product)
                print()
        another = input("Deseja encerrar ou fazer outra pesquisa? "
                        "Se quer fazer outra pesquisa, "
                        "digite \"sim\" sem aspas. Se não, digite qualquer "
                        "outra coisa: ")
        if another.lower().strip() in "sim":
            print()
            continue
        break
