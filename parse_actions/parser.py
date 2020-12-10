from action import Act
import sys
from pprint import pprint
# from parse_actions.action import Action
# from action import Action
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


def print_token(i, tokens):
    t = tokens[i]
    h_i = int(t.head_id.split('_')[1]) - 1

    line = f'{t.id}:{t.head_id} - ({t.rel}) {t.text}'
    line += ' ' * (35 - len(line))
    line += f' <-- {tokens[h_i].text}' if h_i >= 0 else ' ------ ROOT'

    print(line)


text = enter_sentence()
doc = parse_syntax(text)

print_deps(doc)

tokens = list(doc.sents[0].syntax.tokens)

print()

action = Act()
action.detect_root(tokens)
action.detect_subject(tokens)
action.print()

print()

for i, t in enumerate(tokens):
    print_token(i, tokens)

print()
