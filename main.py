#! /usr/bin/env python
import requests
import logging
from utils.constants import MAITRON_BASE_URL
from utils.helpers import is_valid_article
from utils.scrapper import scrape_article, scrape_urls
from utils.semantizer import semantize
from utils.locator import locate
from utils.injector import inject
from utils.database import *

logging.basicConfig(level=logging.INFO)


def main():
    max_iterations = input(
        "Maximum articles: ")

    article_urls = scrape_urls(int(max_iterations))

    for article_url_id in range(0, len(article_urls)):
        article = requests.get(article_urls[article_url_id])
        is_valid = is_valid_article(article.status_code, article.text)
        logging.info(' URL %s is valid : %s',
                     article_urls[article_url_id], is_valid)

        if is_valid:
            scrapped_article = scrape_article(article.text)
            semantized_locations = semantize(scrapped_article)
            locations_coordonnates = locate(semantized_locations)
            data = scrapped_article
            data['locations'] = locations_coordonnates
            inject(data, article_urls[article_url_id])

    logging.info(' Process finished')


if __name__ == '__main__':
    main()
