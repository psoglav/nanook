import json
import pickle
import nltk


lemmatizer = nltk.stem.WordNetLemmatizer()
patterns = json.loads(open('datasets/intro_patterns.json').read())
words = []
documents = []
ignore_letters = list('?.,!')

for pattern in patterns['intro']:
    word_list = nltk.word_tokenize(pattern)
    words.extend(word_list)
    documents.append((word_list, 1))

for pattern in patterns['not']:
    word_list = nltk.word_tokenize(pattern)
    words.extend(word_list)
    documents.append((word_list, 0))

words = [lemmatizer.lemmatize(word)
         for word in words if word not in ignore_letters]

words = sorted(set(words))

pickle.dump(words, open('dump/intro_words.pkl', 'wb'))
pickle.dump(documents, open('dump/intro_patterns.pkl', 'wb'))
