import random
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

import dataset_preparation as d

training = []
output_empty = [0] * len(d.classes)

for document in d.documents:
  bag = []
  word_patterns = document[0]
  word_patterns = [d.lemmatizer.lemmatize(word.lower()) for word in word_patterns]

  for word in d.words:
    bag.append(1 if word in word_patterns else 0)
    
  output_row = list(output_empty)
  output_row[d.classes.index(document[1])] = 1
  training.append([bag, output_row])
  
random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

sgd = SGD(lr=0.01, decay=1e-7, momentum=0.9, nesterov=True)

model = Sequential([
  Dense(128, input_shape=(len(train_x[0]), ), activation='relu'),
  Dropout(0.5),
  Dense(64, activation='relu'),
  Dropout(0.5),
  Dense(len(train_y[0]), activation='softmax'),
])

model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
