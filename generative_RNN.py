import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import utils
import sys

data_filenames = ['data/nfl_game_stats_2009_annotated_clean.csv', 'data/nfl_game_stats_2010_annotated_clean.csv',
                  'data/nfl_game_stats_2011_annotated_clean.csv', 'data/nfl_game_stats_2012_annotated_clean.csv',
                  'data/nfl_game_stats_2013_annotated_clean.csv', 'data/nfl_game_stats_2014_annotated_clean.csv',
                  'data/nfl_game_stats_2015_annotated_clean.csv', 'data/nfl_game_stats_2016_annotated_clean.csv']
headlines = utils.extract_headlines(data_filenames)

def split_by_chars():
    vocab = utils.create_char_vocabulary(headlines)
    start_symbol = utils.START_SYMBOL
    end_symbol = utils.END_SYMBOL
    assert start_symbol not in vocab #choose another symbol if already in vocab
    assert end_symbol not in vocab #choose another symbol if already in vocab
    vocab[start_symbol] = len(vocab)
    vocab[end_symbol] = len(vocab)
    seq_len = 50
    dataX = []
    dataY = []
    for headline in headlines:
        #pad headline
        headline = start_symbol*seq_len + headline + end_symbol
        for i in range(0, len(headline)-seq_len):
            input = headline[i:i+seq_len]
            output = headline[i+seq_len]
            dataX.append([vocab[char] for char in input])
            dataY.append(vocab[output])

    X = np.reshape(dataX, (len(dataX), seq_len, 1))
    X = X / float(len(vocab))
    #one-hot encoding
    y = np_utils.to_categorical(dataY)
    return X, dataX, y, vocab

def split_by_words():
    vocab = utils.create_vocabulary(headlines)
    start_word = utils.START_WORD
    end_word = utils.END_WORD
    vocab[start_word] = len(vocab)
    vocab[end_word] = len(vocab)
    seq_len = 6
    dataX = []
    dataY = []
    for headline in headlines:
        #pad headline
        headline = (start_word+" ")*seq_len + headline + " " + end_word
        headline = headline.split()
        for i in range(0, len(headline)-seq_len):
            input = headline[i:i+seq_len]
            output_word = headline[i+seq_len]
            dataX.append([vocab[utils.clean_word(word)] for word in input])
            dataY.append(vocab[utils.clean_word(output_word)])

    X = np.reshape(dataX, (len(dataX), seq_len, 1))
    X = X / float(len(vocab))
    #one-hot encoding
    y = np_utils.to_categorical(dataY)
    return X, dataX, y, vocab

def create_model(X):

    #LSTM model
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    # model.add(LSTM(128))
    # model.add(Dropout(0.2))
    # model.add(LSTM(64))
    # model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    return model

def train_model(model, X, y, nepoch=20):
    #checkpoints
    filepath="data/checkpoints/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor="loss", verbose=1, save_best_only=True, mode="min")
    callbacks_list = [checkpoint]
    model.fit(X, y, nb_epoch=nepoch, batch_size=128, callbacks=callbacks_list)
    return model


def predict_headline_char(seed, model, checkpoint_file, vocab):
    vocab_lookup = dict((vocab[char], char) for char in vocab.keys())
    model.load_weights(checkpoint_file)
    model.compile(loss="categorical_crossentropy", optimizer='adam')
    print "Seed:", seed
    pattern = [vocab[char] for char in seed]
    output = ""
    for i in range(100):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(len(vocab))
        prediction = model.predict(x, verbose=0)
        index = np.argmax(prediction)
        result = vocab_lookup[index]
        if result == utils.END_SYMBOL:
            return output
        output += result
        pattern.append(index)
        pattern = pattern[1:]
    return output

def predict_headline_word(seed, model, checkpoint_file, vocab):
    vocab_lookup = dict((vocab[char], char) for char in vocab.keys())
    model.load_weights(checkpoint_file)
    model.compile(loss="categorical_crossentropy", optimizer='adam')
    print "Seed:", seed
    pattern = [vocab[word] for word in seed.split()]
    output = ""
    for i in range(100):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(len(vocab))
        prediction = model.predict(x, verbose=0)
        index = np.argmax(prediction)
        result = vocab_lookup[index]
        if result == utils.END_WORD:
            return output
        output += result+" "
        pattern.append(index)
        pattern = pattern[1:]
    return output


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        try:
            nepoch = int(sys.argv[1])
        except:
            print "usage: number of epochs. Defaulting to 20 epochs"
            nepoch = 20
    else:
        nepoch = 20
    X, dataX, y, vocab = split_by_chars()
    model = create_model(X)
    # model = train_model(model, X, y, nepoch)
    # char_filename = 'data/checkpoints/char_encoding/weights-improvement-18-0.5681.hdf5'
    word_filename = 'data/checkpoints/char_encoding/weights-improvement-19-0.4840.hdf5'
    #word_seed = ((utils.START_WORD+" ")*6).strip()
    char_seed = utils.START_SYMBOL*50
    print predict_headline_char(char_seed, model, word_filename, vocab)

