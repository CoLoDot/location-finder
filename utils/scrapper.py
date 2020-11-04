#! /usr/bin/env python
import requests
from bs4 import BeautifulSoup
from .constants import MAITRON_BASE_URL, MAITRON_ARTICLES_BY_PAGE


def scrape_article(article: str) -> dict:
    soup = BeautifulSoup(article, 'html.parser')
    article_title = soup.find("h1", "notice-titre")
    article_intro = soup.find("div", "intro")
    article_content = soup.find("div", "notice-texte entry")

    result = {
        'name': article_title.get_text(),
        'intro': article_intro.get_text(),
        'bio': article_content.get_text(),
        'locations': [],
    }

    return result


def scrape_urls(max_articles: int) -> list:
    urls = []

    for step in range(0, max_articles, MAITRON_ARTICLES_BY_PAGE):
        path = MAITRON_BASE_URL + "/spip.php?mot21&debut_articles=" + \
            str(step) + "#pagination_articles"
        response = requests.get(path)

        soup = BeautifulSoup(response.text, 'html.parser')
        urls_container = soup.find("div", "entry")

        for tag in urls_container.children:
            if tag.name == 'ul':
                for sub_tag in tag.children:
                    if sub_tag.name == 'li':
                        for sub_sub_tag in sub_tag.children:
                            if sub_sub_tag.name == 'a':
                                if len(urls) == max_articles:
                                    break
                                urls.append(MAITRON_BASE_URL +
                                            sub_sub_tag['href'])

    return urls
