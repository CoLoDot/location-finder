#! /usr/bin/env python
import spacy


nlp = spacy.load('fr_core_news_sm')


def semantize(article) -> set:
    treat = nlp(article.get('intro') + article.get('bio'))
    return list(set([t.text for t in treat.ents if t.label_ == 'LOC']))
