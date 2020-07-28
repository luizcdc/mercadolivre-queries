"""Extracts the categories names and codes to categories.pickle."""

from requests import get
from bs4 import BeautifulSoup
import re
import pickle

match_subdomain = re.compile(r"(https://|^)(\w*)\.")
match_suffix = re.compile(r".com.br/(.*)$")


def get_subdomain(link):
    """Extract category subdomain from its url."""
    return match_subdomain.search(link).group(2)


def get_suffix(link):
    """Extract category suffix from its url."""
    return match_suffix.search(link).group(1)


cat_page = BeautifulSoup(
    get("https://www.mercadolivre.com.br/categorias").text,
    "html.parser")

master_categories = cat_page.findAll(class_="categories__container")

categories = [[[0, 'Todas as categorias'], [
    {'subdomain': 'lista', 'suffix': '', 'number': 0, 'name': 'Todas'}]]]
for n1, cat_container in enumerate(master_categories, 1):
    categories.append(
        [
            [n1, cat_container.find(
                'a', class_="categories__title").text], [
                {"number": n2,
                 "name": x.text,
                 "suffix": get_suffix(x["href"]),
                 "subdomain": get_subdomain(x["href"])}
                for n2, x in enumerate(cat_container.find(
                    class_="categories__list").find_all(
                    class_="categories__subtitle"), 1)]])

with open("categories.pickle", "wb") as savefile:
    pickle.dump(categories, savefile)
