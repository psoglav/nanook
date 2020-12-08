import sys
import random
import json
import pickle
import nltk
import numpy as np
import regex as re

from tensorflow.keras.models import load_model
from dataset_preparation import lemmatizer


intents = json.loads(open('datasets/intents.json').read())
words = pickle.load(open('dump/words.pkl', 'rb'))
classes = pickle.load(open('dump/classes.pkl', 'rb'))

if len(sys.argv) > 1:
  model = load_model(sys.argv[1] +'.h5')
else:
  print('Error: provide a training model name')
  exit()


def clean_up_sentence(s):
    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(word) for word in s_words]
    return s_words


def bag_of_words(s):
    s_words = clean_up_sentence(s)
    bag = [0] * len(words)

    for w in s_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)


def splice_sentences(s):
    sentences = re.split(r'[.?!]', s)
    return [sentence for sentence in sentences if sentence]


def predict_class(s):
    result = []

    for sentence in splice_sentences(s):
        bow = bag_of_words(sentence)
        prediction = model.predict(np.array([bow]))[0]
        error_threshold = 0.25
        predictions = [[i, p]
                       for i, p in enumerate(prediction) if p > error_threshold]

        predictions.sort(key=lambda x: x[1], reverse=True)
        mapped_predictions = []
        for p in predictions:
            mapped_predictions.append({
                'intent': classes[p[0]],
                'probability': str(p[1])
            })

        result.append(mapped_predictions)

    return result


def get_reply(intents_lists, intents_json):
    result = ''

    for intents_list in intents_lists:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']

        for i in list_of_intents:
            if i['tag'] == tag:
                result += random.choice(i['replies']) + ' '
                break

    return result


print()
print()
print('chatbot is running!')

while 1:
    message = input('you: ')
    ints = predict_class(message)
    res = get_reply(ints, intents)

    print('bot: ' + res)
