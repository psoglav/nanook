import sys
from pprint import pprint
from natasha import (
    Doc,
    NewsSyntaxParser,
    Segmenter,
    NewsEmbedding
)


segmenter = Segmenter()
emb = NewsEmbedding()
syntax_parser = NewsSyntaxParser(emb)


def enter_sentence():
    text = ''
    inp = '1'

    print()

    while inp:
        inp = ''
        inp = input('предлож.: ')
        text += inp + ' '

    return text


def parse_syntax(sentence):
    doc = Doc(sentence)
    doc.segment(segmenter)
    doc.parse_syntax(syntax_parser)

    return doc


def print_deps(doc):
    print()
    doc.sents[0].syntax.print()
    print()


text = enter_sentence()


doc = parse_syntax(text)
print_deps(doc)

tokens = list(doc.sents[0].syntax.tokens)
tokens = sorted(tokens, key=lambda t: int(t.head_id.split('_')[1]))

root = ''
nsubj = ''
obj = ''
root_t = None
xcomp_t = None


def find_head(child_t, rel=''):
    for t in doc.sents[0].syntax.tokens:
        if rel:
            if t.rel == 'obj' and t.head_id == child_t.id:
                return t
        else:
            if t.head_id == child_t.id:
                return t


for t in doc.sents[0].syntax.tokens:
    if t.rel == 'root':
        root_t = t

for t in doc.sents[0].syntax.tokens:
    if t.rel == 'root':
        root = t.text
    elif t.rel == 'nsubj' and t.head_id == root_t.id:
        nsubj = t.text
    elif t.rel == 'xcomp' and t.head_id == root_t.id:
        xcomp_t = t
    elif t.rel == 'obj' and t.head_id == root_t.id:
        obj = t.text

if xcomp_t:
    for t in doc.sents[0].syntax.tokens:
        if t.rel == 'obl' and t.head_id == xcomp_t.id:
            obj = t.text

print('ДЕЙСТВИЕ: ' + nsubj + ' -> ' + root + ' ' +
      (xcomp_t.text + ' -> ' if xcomp_t else ' -> ') + obj)


print()

for t in doc.sents[0].syntax.tokens:
    i = t.id.split('_')[1]
    head = t.head_id.split('_')[1]

    line = f'{i}: ({t.rel}) {t.text}'
    line = line + (' ' * (25 - len(line)))

    print(line + f' <-- {head}')

print()
