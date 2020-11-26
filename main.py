#! /usr/bin/env python
import requests
import logging
import json
import time
from utils.constants import MAITRON_BASE_URL
from utils.helpers import is_valid_article
from utils.scrapper import scrape_article, scrape_urls
from utils.semantizer import get_birth_and_death_infos, add_dates, get_identity, add_birth_and_death_locations
from utils.locator import locate
from utils.injector import inject
#from utils.database import *
from alive_progress import alive_bar

logging.basicConfig(level=logging.INFO)


def main():
    enable_urls_scrapping = input(
        "Get urls (Y|N): ")
    enable_articles_scrapping = input(
        "Get articles (Y|N): ")
    min_iterations = input(
        "Min article idx: ")
    max_iterations = input(
        "Max article idx (max value 25866 ): ")

    urls = []
    if enable_urls_scrapping == 'Y':
        article_urls = scrape_urls(int(max_iterations))
        _urls = {
            "urls": article_urls
        }
        if len(article_urls):
            with open('urls.json', 'w') as file:
                json_string = json.dumps(
                    _urls, sort_keys=True, indent=4, ensure_ascii=False)
                file.write(json_string)
        urls = _urls.get('urls')
    else:
        with open('utils/dumps/urls.json') as json_file:
            data = json.load(json_file)
            if len(data.get('urls')):
                urls = data['urls']

    articles = []
    scrape_articles = False
    raw_articles = {
        "articles": []
    }
    if enable_articles_scrapping == 'Y':
        scrape_articles = True
    else:
        with open('utils/dumps/articles.json') as json_file:
            data = json.load(json_file)
            if len(data.get('articles')):
                articles = data['articles']

    with alive_bar(int(max_iterations), title='BIOs ', length=100, bar='classic') as bar:
        for article_id in range(int(min_iterations), int(max_iterations)):
            if scrape_articles:
                _article = requests.get(urls[article_id])
                is_valid = is_valid_article(
                    _article.status_code, _article.text)
                if is_valid:
                    scrapped_article = scrape_article(
                        _article.text, article_id, urls[article_id])
                    raw_articles.get("articles").append(scrapped_article)

                    if len(raw_articles.get('articles')):
                        with open('articles.json', 'w') as file:
                            json_string = json.dumps(
                                raw_articles, sort_keys=True, indent=4, ensure_ascii=False)
                            file.write(json_string)
            bar()

    if scrape_articles:
        with open('articles.json') as json_file:
            data = json.load(json_file)
            if len(data.get('articles')):
                articles = data['articles']

    result = []
    # declare your expected total
    with alive_bar(int(max_iterations), title='NLP   ', length=100) as bar:
        for article_id in range(int(min_iterations), int(max_iterations)):
            bar.text('setting up...')
            article = articles[article_id]

            data = {
                "index": article_id,
                "maitron_url": urls[article_id]
            }

            bar.text('getting ID')
            identity = get_identity(article.get('name'))
            data.update(identity)

            bar.text('getting birth & death infos')
            birth_and_death = get_birth_and_death_infos(article)

            bar.text('getting dates')
            dates = add_dates(birth_and_death)
            data.update(dates)

            bar.text('getting locations')
            dates_locations = add_birth_and_death_locations(birth_and_death)
            data.update(dates_locations)

            result.append(data)

            if len(result):
                with open('results.json', 'w') as file:
                    json_string = json.dumps(
                        result, sort_keys=True, indent=4, ensure_ascii=False)
                    bar.text('writting data')
                    file.write(json_string)
            bar()


if __name__ == '__main__':
    main()
