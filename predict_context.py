import nltk as lt
import gensim
from gensim.models import Word2Vec


def flatten(non_flat):
    flat = []

    while non_flat:
        e = non_flat.pop()

        if type(e) == list:
            non_flat.extend(e)
        else:
            flat.append(e)

    flat.reverse()

    return flat


def load_book():
    print('loading book...')
    with open('war_and_peace.txt') as file:
        book = file.readlines()
        book = [line.strip() for line in book if line.strip()]
        book = [lt.sent_tokenize(line) for line in book]
        book = list(flatten(book))
        book = [lt.word_tokenize(line) for line in book]

        print('book loaded!')

        return book


def train_model():
    print('training model...')

    model = Word2Vec(load_book(), min_count=3, size=300)
    print('trained!')

    model.save('word2vec_model_1')
    print('saved!')


def load_model():
    return Word2Vec.load('word2vec_model_1')


model = load_model()

# print(model.wv.most_similar_to_given('gun', ['bullet', 'knife', 'musket']))
# print(model.wv.closer_than('man', 'women'))

# print(lt.pos_tag(lt.word_tokenize('Every sentence you write or speak in English includes words that fall into some of the nine parts of speech. These include nouns, pronouns, verbs, adjectives, adverbs, prepositions, conjunctions, articles/determiners, and interjections.')))
# print(lt.align('super', 'bread'))

# print(gensim.)
