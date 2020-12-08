import random
import pickle
import nltk
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = nltk.stem.WordNetLemmatizer()
documents = pickle.load(open('dump/QA_documents.pkl', 'rb'))
words = pickle.load(open('dump/QA_words.pkl', 'rb'))
answers = [d[1] for d in documents]


training = []
output_empty = [0] * len(documents)

for document in documents:
    bag = []
    question, answer = document
    word_patterns = question
    word_patterns = [lemmatizer.lemmatize(
        word.lower()) for word in word_patterns]

    for word in words:
        bag.append(1 if word in word_patterns else 0)

    output_row = list(output_empty)
    output_row[answers.index(answer)] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

sgd = SGD(lr=0.01, decay=1e-7, momentum=0.9, nesterov=True)

model = Sequential([
    Dense(512, input_shape=(len(train_x[0]), ), activation='relu'),
    Dropout(0.5),
    Dense(254, activation='relu'),
    Dropout(0.5),
    Dense(len(train_y[0]), activation='softmax'),
])

model.compile(loss="categorical_crossentropy",
              optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5, verbose=1)

model.save('models/chatbot_900QA.h5', hist)
