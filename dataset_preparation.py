import json
import pickle
import nltk

lemmatizer = nltk.stem.WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = []
classes = []
documents = []
ignore_letters = list('?.,!')

for intent in intents['intents']:
  for pattern in intent['patterns']:
    word_list = nltk.word_tokenize(pattern)
    words.extend(word_list)
    documents.append((word_list, intent['tag']))
    
    if intent['tag'] not in classes:
      classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('dump\words.pkl', 'wb'))
pickle.dump(classes, open('dump\classes.pkl', 'wb'))