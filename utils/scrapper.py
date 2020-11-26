#! /usr/bin/env python
import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar
from .constants import MAITRON_BASE_URL, MAITRON_ARTICLES_BY_PAGE


def scrape_article(article: str, idx: int, url: str) -> dict:
    _article = {
        'name': '',
        'intro': '',
        'index': idx,
        'maitron_url': url,
    }
    soup = BeautifulSoup(article, 'html.parser')
    article_title = soup.find("h1", "notice-titre")
    article_intro = soup.find("div", "intro")

    if article_title:
        _article['name'] = article_title.get_text()
    if article_intro:
        _article['intro'] = article_intro.get_text()

    return _article


def scrape_urls(max_articles: int) -> list:
    urls = []
    with alive_bar(max_articles, title='URLs ', length=100, bar='circles') as bar:
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
                                    bar()
    return urls
