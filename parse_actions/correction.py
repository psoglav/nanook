import json
import nltk as lt
import regex as re
from pymorphy2 import MorphAnalyzer

conjunctions = json.load(open('datasets/conjunctions.json'))
morph = MorphAnalyzer(lang="ru")


def add_missing_me(s):
    words = lt.word_tokenize(s)

    if 'я' not in words:
        for i, w in enumerate(words):
            w = morph.parse(w)[0]
            if w.tag.POS == 'VERB' and w.tag.person == '1per':
                s = re.sub(w.word, 'я ' + w.word, s)

    return s


def conjs_to_fstops(s):
    # sents = lt.sent_tokenize(s, language="russian")
    for conj in conjunctions:
        s = re.sub(', ' + conj, '. ', s)

    return s


def prepare_for_parsing(text):
    text = conjs_to_fstops(text)
    sents = lt.sent_tokenize(text)
    sents = [add_missing_me(s) for s in sents]

    return ' '.join(sents)
