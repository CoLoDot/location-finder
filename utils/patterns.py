#! /usr/bin/env python
import spacy
from spacy.matcher import Matcher

nlp = spacy.load('fr_core_news_sm')


def date_pattern_matcher(document: str) -> list:
    dates = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "NOUN", "OP": "?"}, {'POS': "NUM"}]
    matcher.add(document, None, pattern)
    doc = nlp(document)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        check = " ".join(dates)
        if not span.text in check:
            dates.append(span.text)

    return " ".join(dates)


def location_pattern_matcher(document: str) -> list:
    places = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "LOC"}]
    matcher.add(document, None, pattern)
    doc = nlp(document)
    matches = matcher(doc)

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        places.append(span.text)

    return " ".join(places)
