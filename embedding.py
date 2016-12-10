from math import exp, floor
import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

from utils import clean_word, extract_column, create_vocabulary, COLUMNS, STATS_COLUMNS, strat, keywords

np.set_printoptions(edgeitems=100, threshold=10000)

class Embedding(object):

    def __init__(self,data_file,train_partition):

        x, y = self.get_data(data_file)
        self.xtrain = x[:int(floor(len(x)*train_partition))]
        self.xtest = x[int(floor(len(x)*train_partition)):]
        self.ytrain = y[:int(floor(len(y)*train_partition))]
        self.ytest = y[int(floor(len(y)*train_partition)):]
        self.headlines_annotated = None

    def set_vocab(self,vocab):

        self.vocab = vocab
        self.vocab_size = len(vocab)

    def get_data(self,file):

        # data files should be of same form
        columns = COLUMNS
        columns_stats = STATS_COLUMNS

        # for experimenting with different feature combination
        columns_test = ['team_1_leader_passing_td','team_1_leader_passing_yds','game_leader_kicker_points','game_leader_scorer_points','team_1_leader_passing_int', \
        'team_2_leader_passing_int','team_score_diff']

        data = pd.read_csv(file, names=columns, sep=',',skiprows=[0])
        headlines_annotated = extract_column([file], 'game_headline_annotated')

        self.set_vocab(create_vocabulary(headlines_annotated))

        # create output y
        y = []
        # Approach 1: frequency counts of words, then softmax
        # for headline in headlines_annotated:
        #     output = np.zeros((self.vocab_size))
        #     headline = headline.split(' ')
        #     for word in headline:
        #         word = clean_word(word)
        #         output[self.vocab[word]] += 1
        #     # apply softmax
        #     output = np.array(map(lambda x: exp(x), output))
        #     output = output / sum(output)
        #     y.append(output)
        # Approach 2: 0/1 words
        # Approach 3: 0/1 Keywords
        KEYWORDS = keywords()
        print len(headlines_annotated)
        for headline in headlines_annotated:
            output = np.zeros((1))
            headline = headline.split(' ')
            for word in headline:
                word = clean_word(word)
                if word in KEYWORDS and word == '[game_leader_scorer]':
                    output[0] = 1
            y.append(output)
        y = np.array(y)
        print len(y)

        # create input x
        x = []
        for index, row in data.iterrows():
            if row['clean_data'] == 1:
                inp = []
                # modify columns_stats to use
                for name in columns_test: 
                    if name == 'team_1_leader_passing_yds':
                        num_buckets = 11
                        yd_buckets = [0] * (num_buckets)
                        index = strat(row[name],[0,50,100,150,200,250,300,350,400,450,500])
                        yd_buckets[index] = 1
                        inp.extend(yd_buckets)
                    elif name == 'game_leader_kicker_points' or name == 'game_leader_scorer_points':
                        num_buckets = 4
                        pt_buckets = [0]*(num_buckets)
                        index = strat(row[name],range(0,num_buckets))
                        pt_buckets[index] = 1
                        inp.extend(pt_buckets)
                    elif name == 'team_score_diff':
                        num_buckets = 5
                        score_diff = abs(row['team_1_score']-row['team_2_score'])
                        score_buckets = [0] * (num_buckets)
                        index = strat(score_diff, [0,2,7,14,21])
                        score_buckets[index] = 1
                        inp.extend(score_buckets)
                    else:
                        inp.append(row[name])

                x.append(inp)
        print x

        # x = v.fit_transform(x).toarray()

        self.headlines_annotated = headlines_annotated
        return (x,y)

    def train(self, loss, learning_rate = 0.01, epochs=20, batch_size=256):
        input_size = len(self.xtrain[0])
        self.vocab_size = len(self.vocab)
        model = Sequential()
        model.add(Dense(input_size,input_dim=input_size))
        model.add(Activation('relu'))
        model.add(Dropout(0.50))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))
        model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])
        model.fit(self.xtrain, self.ytrain, nb_epoch = epochs, batch_size=batch_size)
        self.model = model
        self.is_trained = True

    def predict(self):
        classes = self.model.predict_classes(self.xtest)
        proba = self.model.predict(self.xtest)
        self.prob = proba
        print proba
        return (classes,proba)

    def normalize(self):
        norm = []
        # Approach 1:
        # for p in predictions:
        #     avg = np.average(p)
        #     norm.append(map(lambda x: x if x >= avg else 0, p))
        # Approach 3
        for p in self.prob:
            norm.append(map(lambda x: 1 if x > .65 else 0, p))
        norm = np.array(norm)
        self.norm = norm
        print self.norm
        return norm

    def word_to_prob(self):
        vocab = self.vocab
        norm = self.norm
        prob = self.prob
        probs = []
        # either for vector in prob, or norm
        for vect in prob:
            word_to_prob = {}
            for word in vocab:
                word_to_prob[word] = vect[vocab[word]]
            probs.append(word_to_prob)
        self.word_to_prob = probs
        return probs

if __name__ == '__main__':
    f = 'data/nfl_game_stats_annotated_clean.csv'
    partition = 0.70
    e = Embedding(f,partition)
    e.train('categorical_crossentropy')
    classes, proba = e.predict()
    e.normalize()

    last = e.norm[-10:]

    for item in last:
        for i in range(len(item)):
            if item[i] == 1:
                print keywords()[i]
        print '-----------'


    # print e.norm
    # proba_norm = e.normalize(proba)
    # word_to_prob = e.word_to_prob()