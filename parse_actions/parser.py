import sys
from pprint import pprint
# from parse_actions.action import Action
from action import Action
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


def parse_action(tokens):
    rels = [t.rel for t in tokens]
    passed = []

    action = Action()

    def points(head, t):
        return head.id == t.head_id

    for t in tokens:
        passed.append(t)

        # if t.rel == 'punct' and (''):
            

        if t.rel == 'root':
            action.define_what(t)  # verb

    for t in tokens:
        if t.rel == 'advmod' and points(action._what, t):
            action.define_how(t)  # adverb

        if t.rel == 'nsubj':
            if 'nsubj' in rels:
                action.define_who(t)  # subject

        if t.rel == 'obj':
            if 'nsubj' in rels:
                action.define_whom(t)  # object
            else:
                action.define_who(t)

        if t.rel == 'obl' and points(action._what, t):
            action.define_with(t)  # object

    return action


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


parse_action(doc.sents[0].syntax.tokens).print(heads=True)


print()

for t in doc.sents[0].syntax.tokens:
    i = t.id.split('_')[1]
    head = t.head_id.split('_')[1]

    line = f'{i}: ({t.rel}) {t.text}'
    line = line + (' ' * (25 - len(line)))

    print(line + f' <-- {head}')

print()
