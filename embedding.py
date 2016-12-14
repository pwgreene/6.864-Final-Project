from math import exp, floor
import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

from utils import clean_word, extract_column, create_vocabulary, COLUMNS, STATS_COLUMNS, strat, END_WORD

class Embedding(object):

    def __init__(self,data_file,train_partition):

        self.raw_train = None
        self.raw_test = None
        self.headlines_annotated = None
        x, y = self.get_data(data_file)
        self.xtrain = x[:int(floor(len(x)*train_partition))]
        self.xtest = x[int(floor(len(x)*train_partition)):]
        self.ytrain = y[:int(floor(len(y)*train_partition))]
        self.ytest = y[int(floor(len(y)*train_partition)):]

    def set_vocab(self,vocab):

        self.vocab = vocab
        self.vocab_size = len(vocab)

    def get_data(self,file):

        # data files should be of same form
        columns = COLUMNS
        columns_stats = STATS_COLUMNS

        # for experimenting with different feature combination
        columns_test = ['team_1_leader_passing_td','team_1_leader_passing_yds','team_1_leader_rushing_yds','team_1_leader_rushing_td','team_1_leader_receiving_td','team_1_leader_receiving_yds','game_leader_kicker_points','game_leader_scorer_points','team_1_leader_passing_int', \
        'team_2_leader_passing_int','team_score_diff']

        data = pd.read_csv(file, names=columns, sep=',',skiprows=[0])

        headlines_annotated = extract_column([file], 'game_headline_annotated')
        vocab = create_vocabulary(headlines_annotated)
        vocab[END_WORD] = len(vocab)
        
        self.set_vocab(vocab)
        vector_length = len(self.vocab)
        y = []
        self.vocab_size = vector_length
        for headline in headlines_annotated:
            output = np.zeros((vector_length))
            headline = headline.split(' ')
            for word in headline:
                word = clean_word(word)
                output[vocab[word]] = 1
            output[vocab[END_WORD]] = 1
            # apply softmax
            # output = np.array(map(lambda x: exp(x), output))
            output = output / sum(output)
            y.append(output)

        y = np.array(y)

        raw = []
        for index, row in data.iterrows():
            if row['clean_data'] == 1:
                raw.append(row)

        self.raw_train = raw[:int(floor(len(raw)*0.70))]
        self.raw_test = raw[int(floor(len(raw)*0.70)):]

        # create input x
        x = []
        v = DictVectorizer()
        for index, row in data.iterrows():
            if row['clean_data'] == 1:

                inp = []
                for label in columns_stats:
                    inp.append(row[label])
                # # modify columns_stats to use
                # for name in columns_test:
                #     if name == 'team_1_leader_passing_yds':
                #         num_buckets = 11
                #         yd_buckets = [0] * (num_buckets)
                #         index = strat(row[name],[0,50,100,150,200,250,300,350,400,450,500])
                #         yd_buckets[index] = 1
                #         inp.extend(yd_buckets)
                #     elif name == 'game_leader_kicker_points' or name == 'game_leader_scorer_points':
                #         num_buckets = 4
                #         pt_buckets = [0]*(num_buckets)
                #         index = strat(row[name],range(0,num_buckets))
                #         pt_buckets[index] = 1
                #         inp.extend(pt_buckets)
                #     elif name == 'team_1_leader_rushing_yds' or name == 'team_1_leader_receiving_yds':
                #         num_buckets = 7
                #         yd_buckets = [0] * (num_buckets)
                #         index = strat(row[name],[0,25,50,75,100,125,150])
                #         yd_buckets[index] = 1
                #         inp.extend(yd_buckets)                        
                #     elif name == 'team_score_diff':
                #         num_buckets = 5
                #         score_diff = abs(row['team_1_score']-row['team_2_score'])
                #         score_buckets = [0] * (num_buckets)
                #         index = strat(score_diff, [0,2,7,14,21])
                #         score_buckets[index] = 1
                #         inp.extend(score_buckets)
                #     else:
                #         inp.append(row[name])

                x.append(inp)

        self.headlines_annotated = headlines_annotated
        
        return (x,y)

    def train(self, loss, learning_rate = 0.05, epochs=100, batch_size=256):
        input_size = len(self.xtrain[0])
        model = Sequential()
        model.add(Dense(2*input_size,input_dim=input_size, init='normal'))
        model.add(Activation('relu'))
        model.add(Dropout(0.10))
        model.add(Dense(2*input_size, init='normal', activation='relu'))
        model.add(Dropout(0.10))
        model.add(Dense(2*input_size, init='normal', activation='relu'))
        model.add(Dropout(0.10))
        model.add(Dense(self.vocab_size))
        model.add(Activation('softmax'))
        model.compile(loss=loss, optimizer='adam')
        model.fit(self.xtrain, self.ytrain, nb_epoch = epochs, batch_size=batch_size)
        self.model = model
        self.is_trained = True

    def predict(self):
        classes = self.model.predict_classes(self.xtest)
        proba = self.model.predict(self.xtest)
        self.prob = proba
        return (classes,proba)

    # def normalize(self,predictions):
    #     norm = []
    #     for p in predictions:
    #         avg = np.average(p)
    #         norm.append(map(lambda x: x if x >= avg else 0, p))
    #     norm = np.array(norm)
    #     self.norm = norm

    def word_to_prob(self):
        vocab = self.vocab
        probs = []
        for vect in self.prob:
            word_to_prob = {}
            for word in vocab:
                word_to_prob[word] = vect[vocab[word]]
            probs.append(word_to_prob)
        self.word_to_prob = probs
        return probs

# if __name__ == '__main__':
    # f = 'nfl_game_stats_annotated_clean.csv'
    # partition = 0.70
    # e = Embedding(f,partition)
    # e.train('categorical_crossentropy')
    # classes, proba = e.predict()
    # proba_norm = e.normalize(proba)
    # word_to_prob = e.word_to_prob()
    # print word_to_prob
