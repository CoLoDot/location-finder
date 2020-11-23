#! /usr/bin/env python
import spacy
from spacy.matcher import Matcher
from .locator import locate
from .constants import BIRTH_STOP_WORDS, DEATH_STOP_WORDS, SURNAME_STOP_WORDS
from .patterns import location_pattern_matcher, date_pattern_matcher

nlp = spacy.load('fr_core_news_sm')


def get_birth_and_death_infos(article: dict) -> dict:
    doc = nlp(article.get("intro"))

    lemmas_infos = {
        "birth_lemma": False,
        "death_lemma": False,
        "birth_token": None,
        "death_token": None,
        "birth_token_index": None,
        "death_token_index": None,
    }

    _birth_lemma, _death_lemma = False, False
    for token in doc:
        if _birth_lemma == True and _death_lemma == True:
            break
        if token.lemma_ in BIRTH_STOP_WORDS:
            lemmas_infos["birth_lemma"] = True
            lemmas_infos["birth_token"] = str(token)
            lemmas_infos["birth_token_index"] = token.i
            _birth_lemma = True
        if token.lemma_ in DEATH_STOP_WORDS:
            lemmas_infos["death_lemma"] = True
            lemmas_infos["death_token"] = str(token)
            lemmas_infos["death_token_index"] = token.i
            _death_lemma = True

    if lemmas_infos.get('birth_lemma') == True and lemmas_infos.get('death_lemma') == True:
        lemmas_infos["span_birth"] = str(doc[lemmas_infos.get(
            'birth_token_index'):lemmas_infos.get('death_token_index')])
        lemmas_infos["span_death"] = str(
            doc[lemmas_infos.get('death_token_index'):-1])
    if lemmas_infos.get('birth_lemma') == True and lemmas_infos.get('death_lemma') == False:
        lemmas_infos["span_birth"] = str(
            doc[lemmas_infos.get('birth_token_index'):-1])
    if lemmas_infos.get('birth_lemma') == False and lemmas_infos.get('death_lemma') == True:
        lemmas_infos["span_death"] = str(
            doc[lemmas_infos.get('death_token_index'):-1])

    return lemmas_infos


def add_dates(birth_and_death_infos: dict) -> dict:
    infos = birth_and_death_infos
    dates = {}
    if infos.get("span_birth"):
        dates['birth_date'] = date_pattern_matcher(infos.get("span_birth"))
    if infos.get("span_death"):
        dates['death_date'] = date_pattern_matcher(infos.get("span_death"))

    return dates


def add_birth_and_death_locations(birth_and_death_infos: dict) -> dict:
    infos = birth_and_death_infos
    locations = {}

    if infos.get("span_birth"):
        birth_place = location_pattern_matcher(infos.get("span_birth"))
        locate_birth_place = locate(birth_place)

        locations['birth_place'] = locate_birth_place.get('location')
        locations['birth_place_country'] = locate_birth_place.get('country')
        locations['birth_place_coord'] = locate_birth_place.get(
            'lat') + ',' + locate_birth_place.get('long')

    if infos.get("span_death"):
        death_place = location_pattern_matcher(infos.get("span_death"))
        locate_death_place = locate(death_place)

        locations['death_place'] = locate_death_place.get('location')
        locations['death_place_coord'] = locate_death_place.get(
            'lat') + ',' + locate_death_place.get('long')

    return locations


def get_identity(article_name_section: str) -> dict:
    identity = {}

    doc = nlp(article_name_section)
    _stop_idx = []
    for token in doc:
        if token.is_left_punct:
            _stop_idx.append(token.i)
        if token.is_right_punct:
            _stop_idx.append(token.i)
        if str(token) == 'dit':
            _stop_idx.append(token.i)
        if str(token) == 'pseudonyme':
            _stop_idx.append(token.i)
        if str(token) == 'surnom':
            _stop_idx.append(token.i)
        if str(token) == 'Écrit':
            _stop_idx.append(token.i)
        if str(token) == 'pseudo':
            _stop_idx.append(token.i)

    limit = sorted(_stop_idx)

    if len(limit):
        span = doc[:limit[0]]
        identity['last_name'] = ", ".join([str(token)
                                           for token in span if token.is_upper])
        identity['first_name'] = " ".join([str(token)
                                           for token in span if not token.is_upper and not token.is_punct])
    else:
        identity['last_name'] = ", ".join(
            [str(token) for token in doc if token.is_upper])
        identity['first_name'] = " ".join([str(token)
                                           for token in doc if not token.is_upper and not token.is_punct])

    return identity
