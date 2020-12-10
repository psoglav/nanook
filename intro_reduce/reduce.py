import sys
import random
import json
import pickle
import nltk
import numpy as np
import regex as re

from tensorflow.keras.models import load_model

lemmatizer = nltk.stem.WordNetLemmatizer()

documents = pickle.load(open('dump/intro_patterns.pkl', 'rb'))
words = pickle.load(open('dump/intro_words.pkl', 'rb'))

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


def predict_class(s):
    bow = bag_of_words(s)
    prediction = model.predict(np.array([bow]))[0]
    error_threshold = 0.25
    predictions = [[i, p]
                    for i, p in enumerate(prediction) if p > error_threshold]

    predictions.sort(key=lambda x: x[1], reverse=True)
    mapped_predictions = []
    for p in predictions:
        mapped_predictions.append({
            'intro': p[0],
            'probability': str(p[1])
        })

    return mapped_predictions


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
    res = predict_class(message)
    # res = get_reply(ints, intents)

    print('prediction is: ' + ['НЕ вводная фраза','вводная фраза'][res[0]['intro']])
    print()
