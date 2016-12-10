import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from math import exp, floor
from markov import clean_word

def strat(val,ranges):
    for i in range(1,len(ranges)):
        lo, hi = ranges[i-1], ranges[i]
        if val > lo and val <= hi:
            return i-1
    return len(ranges)-1

class Embedding(object):

    def __init__(self,data_file,train_partition):

        self.headlines_annotated = None
        x, y = self.get_data(data_file)
        self.xtrain = x[:int(floor(len(x)*train_partition))]
        self.xtest = x[int(floor(len(x)*train_partition)):]
        self.ytrain = y[:int(floor(len(y)*train_partition))]
        self.ytest = y[int(floor(len(y)*train_partition)):]

    def set_vocab(self,vocab):
        self.vocab = vocab

    # todo: modify to allow concatenation of various data files
    def get_data(self,file):

        # data files should be of same form
        columns = ['game_year','game_week','team_1_abbr','team_1_city','team_1_mascot','team_1_score', \
                   'team_1_leader_passing','team_1_leader_passing_yds','team_1_leader_passing_td','team_1_leader_passing_int', \
                   'team_1_leader_rushing','team_1_leader_rushing_yds','team_1_leader_rushing_td','team_1_leader_receiving', \
                   'team_1_leader_receiving_yds','team_1_leader_receiving_td','team_2_abbr','team_2_city','team_2_mascot', \
                   'team_2_score','team_2_leader_passing','team_2_leader_passing_yds','team_2_leader_passing_td','team_2_leader_passing_int', \
                   'team_2_leader_rushing','team_2_leader_rushing_yds','team_2_leader_rushing_td','team_2_leader_receiving','team_2_leader_receiving_yds', \
                   'team_2_leader_receiving_td','game_leader_scorer','game_leader_scorer_points','game_leader_kicker','game_leader_kicker_points', \
                   'game_headline','game_headline_annotated','clean_data','team_score_diff']
        columns_stats = ['team_1_score', 'team_1_leader_passing_yds','team_1_leader_passing_td','team_1_leader_passing_int', \
                   'team_1_leader_rushing_yds','team_1_leader_rushing_td','team_1_leader_receiving_yds','team_1_leader_receiving_td', \
                   'team_2_score','team_2_leader_passing_yds','team_2_leader_passing_td','team_2_leader_passing_int', \
                   'team_2_leader_rushing_yds','team_2_leader_rushing_td','team_2_leader_receiving_yds', \
                   'team_2_leader_receiving_td','game_leader_scorer_points','game_leader_kicker_points', 'team_score_diff']
        columns_test = ['team_1_leader_passing_td','team_1_leader_passing_yds','game_leader_kicker_points','game_leader_scorer_points','team_1_leader_passing_int', \
        'team_2_leader_passing_int','team_score_diff',]
        data = pd.read_csv(file, names=columns, sep=',',skiprows=[0])
        headlines_annotated = [data['game_headline_annotated'][i] for i in \
        range(len(data['game_headline_annotated'])) if data['clean_data'][i]]

        # create output y
        y = []
        vocab = {}
        index = 0
        # get vocabulary to have indices of words
        for headline in headlines_annotated:
            headline = headline.split(' ')
            for word in headline:
                word = clean_word(word)
                if word not in vocab:
                    vocab[word] = index
                    index += 1
        self.set_vocab(vocab)
        # print len(vocab)
        vector_length = len(vocab)

        self.vocab_size = vector_length
        for headline in headlines_annotated:
            output = np.zeros((vector_length))
            headline = headline.split(' ')
            for word in headline:
                word = clean_word(word)
                output[vocab[word]] += 1
            # apply softmax
            output = np.array(map(lambda x: exp(x), output))
            output = output / sum(output)
            y.append(output)
        y = np.array(y)

        # create input x
        x = []
        v = DictVectorizer()
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
        # x = v.fit_transform(x).toarray()

        self.headlines_annotated = headlines_annotated
        return (x,y)

    def train(self, loss, learning_rate = 0.01, epochs=20, batch_size=256):
        input_size = len(self.xtrain[0])
        self.vocab_size = len(self.vocab)
        model = Sequential()
        model.add(Dense(2*input_size,input_dim=input_size))
        model.add(Activation('relu'))
        model.add(Dropout(0.25))
        model.add(Dense(self.vocab_size))
        model.add(Activation('softmax'))
        sgd = SGD(lr=learning_rate)
        model.compile(loss=loss, optimizer=sgd)
        model.fit(self.xtrain, self.ytrain, nb_epoch = epochs, batch_size=batch_size)
        self.model = model
        self.is_trained = True

    def predict(self):
        classes = self.model.predict_classes(self.xtest)
        proba = self.model.predict_proba(self.xtest)
        print proba
        self.prob = proba
        return (classes,proba)

    def normalize(self,predictions):
        norm = []
        for p in predictions:
            avg = np.average(p)
            norm.append(map(lambda x: x if x >= avg else 0, p))
        norm = np.array(norm)
        self.norm = norm
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
    f = 'nfl_game_stats_annotated_clean.csv'
    partition = 0.70
    e = Embedding(f,partition)
    e.train('categorical_crossentropy')
    classes, proba = e.predict()
    print proba
    # proba_norm = e.normalize(proba)
    # word_to_prob = e.word_to_prob()
