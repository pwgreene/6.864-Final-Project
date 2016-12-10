import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import utils
import sys

master_file = 'data/nfl_game_stats_annotated_clean.csv'
data_filenames = ['data/nfl_game_stats_2009_annotated_clean.csv', 'data/nfl_game_stats_2010_annotated_clean.csv',
                  'data/nfl_game_stats_2011_annotated_clean.csv', 'data/nfl_game_stats_2012_annotated_clean.csv',
                  'data/nfl_game_stats_2013_annotated_clean.csv', 'data/nfl_game_stats_2014_annotated_clean.csv',
                  'data/nfl_game_stats_2015_annotated_clean.csv', 'data/nfl_game_stats_2016_annotated_clean.csv']
headlines = utils.extract_column(master_file, 'game_headline_annotated')
features = utils.get_features(master_file)
print len(headlines), len(features)
assert len(headlines) == len(features)

def split_by_chars(seq_len, features=None):
    vocab = utils.create_char_vocabulary(headlines)
    start_symbol = utils.START_SYMBOL
    end_symbol = utils.END_SYMBOL
    assert start_symbol not in vocab #choose another symbol if already in vocab
    assert end_symbol not in vocab #choose another symbol if already in vocab
    vocab[start_symbol] = len(vocab)
    vocab[end_symbol] = len(vocab)
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

def split_by_chars_with_features(seq_len, features=None):
    vocab = utils.create_char_vocabulary(headlines)
    start_symbol = utils.START_SYMBOL
    end_symbol = utils.END_SYMBOL
    assert start_symbol not in vocab #choose another symbol if already in vocab
    assert end_symbol not in vocab #choose another symbol if already in vocab
    vocab[start_symbol] = len(vocab)
    vocab[end_symbol] = len(vocab)
    dataX = []
    dataY = []
    for i in range(len(headlines)):
        #pad headline
        headline = start_symbol*seq_len + headlines[i] + end_symbol
        for j in range(0, len(headline)-seq_len):
            input = headline[j:j+seq_len]
            output = headline[j+seq_len]
            dataX.append([vocab[char] for char in input]+features[i])
            dataY.append(vocab[output])

    X = np.reshape(dataX, (len(dataX), seq_len+len(features), 1))
    X = X / float(len(vocab))
    #one-hot encoding
    y = np_utils.to_categorical(dataY)
    return X, dataX, y, vocab

def split_by_words(seq_len):
    vocab = utils.create_vocabulary(headlines)
    start_word = utils.START_WORD
    end_word = utils.END_WORD
    vocab[start_word] = len(vocab)
    vocab[end_word] = len(vocab)
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

def create_model(X, y):

    #LSTM model
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    return model

def train_model(model, X, y, is_words, nepoch=20):
    #checkpoints
    if is_words:
        filepath="data/checkpoints/word_encoding/words-{loss:.4f}.hdf5"
    else:
        filepath="data/checkpoints/char_encoding/chars-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor="loss", verbose=1, save_best_only=True, mode="min")
    callbacks_list = [checkpoint]
    model.fit(X, y, nb_epoch=nepoch, batch_size=128, callbacks=callbacks_list)
    return model


def predict_headline_char(seed, model, checkpoint_file, vocab, temperature=0.25):
    vocab_lookup = dict((vocab[char], char) for char in vocab.keys())
    model.load_weights(checkpoint_file)
    model.compile(loss="categorical_crossentropy", optimizer='adam')
    #print "Seed:", seed
    pattern = [vocab[char] for char in seed]
    output = ""
    for i in range(100):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(len(vocab))
        prediction = model.predict(x, verbose=0)[0]
        index = sample_probabilities(prediction, temperature)
        #index = np.argmax(prediction)
        result = vocab_lookup[index]
        if result == utils.END_SYMBOL:
            return output
        output += result
        pattern.append(index)
        pattern = pattern[1:]
    return output

def predict_headline_word(seed, model, checkpoint_file, vocab, temperature=0.2):
    vocab_lookup = dict((vocab[char], char) for char in vocab.keys())
    model.load_weights(checkpoint_file)
    model.compile(loss="categorical_crossentropy", optimizer='adam')
    #print "Seed:", seed
    pattern = [vocab[word] for word in seed.split()]
    output = ""
    for i in range(20):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(len(vocab))
        probs = model.predict(x, verbose=0)[0]
        index = sample_probabilities(probs, temperature)
        #index = np.argmax(prediction)
        result = vocab_lookup[index]
        if result == utils.END_WORD:
            return output
        output += result+" "
        pattern.append(index)
        pattern = pattern[1:]
    return output

def sample_probabilities(probs, temp):
    x = np.log(probs)/temp
    x = np.exp(x)
    x *= 1./np.sum(x)
    #print np.random.multinomial()
    return np.argmax(np.random.multinomial(1, x*.99999, size=1))

def create_summary_by_words(nepoch, ntrials, seq_len, train=False):
    X, dataX, y, vocab = split_by_words(seq_len)
    model = create_model(X, y)
    if train:
        model = train_model(model, X, y, True, nepoch)
        filename = raw_input("[prompt] enter filename of best model: ")
    else:
        filename = 'data/checkpoints/word_encoding/words-3.7061.hdf5'
    seed = ((utils.START_WORD+" ")*seq_len).strip()
    ntrials = 10
    for trial in range(ntrials):
        print predict_headline_word(seed, model, filename, vocab)
        print

def create_summary_by_chars(nepoch, ntrials, seq_len, train=False, add_features=False):
    if add_features:
        X, dataX, y, vocab = split_by_chars_with_features(seq_len, features)
    else:
        X, dataX, y, vocab = split_by_chars(seq_len)
    model = create_model(X, y)
    if train:
        model = train_model(model, X, y, False, nepoch)
        filename = raw_input("[prompt] enter filename of best model: ")
    else:
        filename = 'data/checkpoints/char_encoding/weights-improvement-19-0.4840.hdf5'
    seed = utils.START_SYMBOL*seq_len
    ntrials = 10
    for trial in range(ntrials):
        print predict_headline_word(seed, model, filename, vocab)
        print


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        try:
            nepoch = int(sys.argv[1])
        except:
            print "usage: number of epochs. Defaulting to 20 epochs"
            nepoch = 20
    else:
        nepoch = 20

    create_summary_by_chars(nepoch, 10, seq_len=50, train=True, add_features=True)

