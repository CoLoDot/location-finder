#! /usr/bin/env python
import requests
from bs4 import BeautifulSoup
from .constants import MAITRON_BASE_URL


def scrape(article: str) -> dict:
    soup = BeautifulSoup(article, 'html.parser')
    article_title = soup.find("h1", "nom-notice")
    article_intro = soup.find("div", "chapo")
    article_content = soup.find("div", "texte")

    result = {
        'name': article_title.get_text(),
        'intro': article_intro.get_text(),
        'bio': article_content.get_text(),
        'locations': [],
    }

    return result
