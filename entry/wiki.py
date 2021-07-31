import random
from typing import Union
from urllib import request
from http.client import HTTPResponse

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString


def random_paragraph() -> str:
    paragraphs = random_article()
    return random.choice(paragraphs)


def random_article() -> [str]:
    with request.urlopen("https://en.wikipedia.org/wiki/Special:Random") as response:
        response: HTTPResponse
        page = response.read().decode("UTF-8")

    doc = BeautifulSoup(page, "html.parser")
    print(f'Article title: "{doc.find(id="firstHeading").text}"')
    article = doc.find(id="mw-content-text")

    for meta in article.find_all(class_="metadata"):
        meta.extract()

    paragraphs = [_clean_text(p) for p in article.find_all("p")]

    # Find paragraphs of at least 50 characters.
    # If there are none, lower the length requirement by 10 until there is at least one.
    filtered = list()
    min_length = 50

    while len(filtered) == 0:
        filtered = [p for p in paragraphs if len(p) > min_length]
        min_length -= 10

    return filtered


def _clean_text(element: Union[Tag, NavigableString]) -> str:
    # Remove references like "[1]"
    for sup in element.find_all("sup", class_="reference"):
        sup.extract()

    text = element.text

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()
