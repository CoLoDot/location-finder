#! /usr/bin/env python
import requests
import logging
from utils.constants import MAITRON_BASE_URL
from utils.helpers import is_valid_article
from utils.scrapper import scrape
from utils.semantizer import semantize
from utils.locator import locate
from utils.injector import inject
from utils.database import *

logging.basicConfig(level=logging.INFO)


def main():
    max_maitron_article_id = input(
        "Maximum iterations: ")

    min_maitron_article_id = 540
    for article_id in range(0, int(max_maitron_article_id)):
        article = requests.get(
            MAITRON_BASE_URL + str(min_maitron_article_id + article_id))
        is_valid = is_valid_article(article.status_code, article.text)

        logging.info(' ID %s is valid : %s', str(
            min_maitron_article_id + article_id), is_valid)

        if is_valid:
            scrapped_article = scrape(article.text)
            semantized_locations = semantize(scrapped_article)
            locations_coordonnates = locate(semantized_locations)
            data = scrapped_article
            data['locations'] = locations_coordonnates
            inject(data)

        if article_id == int(max_maitron_article_id):
            break


if __name__ == '__main__':
    main()
