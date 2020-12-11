import nltk
from parse_actions.action import Act
from parse_actions.correction import prepare_for_parsing
from natasha import (
    Doc,
    NewsSyntaxParser,
    Segmenter,
    NewsEmbedding
)


segmenter = Segmenter()
emb = NewsEmbedding()
syntax_parser = NewsSyntaxParser(emb)


def enter_text():
    text = ''
    inp = '1'

    while inp:
        inp = input('text: ')
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


def print_tokens(tokens):
    for t in tokens:
        h_i = int(t.head_id.split('_')[1]) - 1

        line = f'{t.id}:{t.head_id} - ({t.rel}) {t.text}'
        line += ' ' * (35 - len(line))
        line += f' <-- {tokens[h_i].text}' if h_i >= 0 else ' ------ ROOT'

        print(line)

doc = ''
tokens = ''

while 1:
    text = enter_text()
    print()
    text = prepare_for_parsing(text)

    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:
        doc = parse_syntax(sentence)
        tokens = list(doc.sents[0].syntax.tokens)

        action = Act()
        action.detect_root(tokens)
        action.detect_subject(tokens)
        action.detect_object(tokens)
        action.detect_xcomp(tokens)
        act = action.compose()
        
        if not act:
            continue
        
        # print(f'({sentence.strip()})')
        print(act)
    print()
    # if sentences:
        # print_deps(doc)
    # print()

    print()
    if tokens: print_tokens(tokens)
