import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    assert(len(series) >= window_size + 1)
    # containers for input/output pairs
    X = [[series[j] for j in range(i - window_size, i)] for i in range(window_size, len(series))]
    y = [series[i] for i in range(window_size, len(series))]

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))
    
    return model
    
### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    punctuation = set(['!', ',', '.', ':', ';', '?'])
    text_unique_chars = set()
    
    for char in text:
        text_unique_chars.add(char)
        
    replace_chars = [c for c in text_unique_chars if not c.isalpha() and c not in punctuation]
    
    for char in replace_chars:
        text = text.replace(char, ' ')
        
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    pass
