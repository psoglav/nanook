import json
import pickle
import nltk
from pprint import pprint

lemmatizer = nltk.stem.WordNetLemmatizer()
intents = json.loads(open('datasets/QA.json').read())
words = []
answers = [intent['answer'] for intent in intents]
questions = [intent['question'] for intent in intents]
documents = []
ignore_letters = list('?.,! ')

for i, q in enumerate(questions):
    question = nltk.word_tokenize(q)
    
    words.extend(question)
    
    documents.append((question, answers[i], ))

words = [lemmatizer.lemmatize(w)
         for w in words if w not in ignore_letters]

words = sorted(set(words))

pickle.dump(documents, open('dump/QA_documents.pkl', 'wb'))
pickle.dump(words, open('dump/QA_words.pkl', 'wb'))

print('Dumped!')
