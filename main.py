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

logging.basicConfig(level=logging.INFO)


def main():
    max_iterations = input(
        "Maximum articles: ")

    article_urls = scrape_urls(int(max_iterations))

    result = []
    for article_url_id in range(0, len(article_urls)):
        article = requests.get(article_urls[article_url_id])
        is_valid = is_valid_article(article.status_code, article.text)
        logging.info(' ID: %s URL %s is valid : %s', article_url_id,
                     article_urls[article_url_id], is_valid)

        if is_valid:
            data = {
                "maitron_url": article_urls[article_url_id]
            }
            scrapped_article = scrape_article(article.text)
            identity = get_identity(scrapped_article.get('name'))
            # need to add surname if exists
            data.update(identity)
            birth_and_death = get_birth_and_death_infos(scrapped_article)
            dates = add_dates(birth_and_death)
            data.update(dates)
            dates_locations = add_birth_and_death_locations(birth_and_death)
            data.update(dates_locations)
            result.append(data)

            if len(result):
                with open('result.json', 'w') as file:
                    json_string = json.dumps(
                        result, sort_keys=True, indent=4, ensure_ascii=False)
                    file.write(json_string)

    logging.info(' Process finished')


if __name__ == '__main__':
    start_time = time.time()
    main()
    logging.info(' Execution time : %s seconds', time.time() - start_time)
