import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

class Embedding(object):

        def __init__(self,data_file,train_partition):
		
                x, y = get_data(data_file)
                self.xtrain = x[:len(x)*train_partition]
                self.xtest = x[len(x)*train_partition:]
                self.ytrain = y[:len(y)*train_partition]
                self.ytest = y[len(y)*train_partition:]

                self.model = None
                self.is_trained = False
                self.vocab_size = 0
                
        # todo: modify to allow concatenation of various data files
	def get_data(self,file):
		
                # data files should be of same form
		columns = ['game_year','game_week','team_1_abbr','team_1_city','team_1_mascot','team_1_score', \
		'team_1_leader_passing','team_1_leader_passing_yds','team_1_leader_passing_td','team_1_leader_passing_int', \
		'team_1_leader_rushing','team_1_leader_rushing_yds','team_1_leader_rushing_td','team_1_leader_receiving', \
		'team_1_leader_receiving_yds','team_1_leader_receiving_td','team_2_abbr','team_2_city','team_2_mascot', \
		'team_2_score','team_2_leader_passing','team_2_leader_passing_yds','team_2_leader_passing_td','team_2_leader_passing_int', \
		'team_2_leader_rushing','team_2_leader_rushing_yds','team_2_leader_rushing_td','team_2_leader_receiving','team_2_leader_receiving_yds', \
		'team_2_leader_receiving_td','game_leader_scorer','game_leader_scorer_points','game_leader_kicker','game_leader_kicker_points',\
		'game_headline','game_headline_annotated','clean_data']
		data = pd.read_csv(file, names=columns, sep=',',skiprows=[0])
                headlines_annotated = list(data['game_headline_annotated'])
		
                # create output y
		y = []
                vocab = {}
                index = 0
                # get vocabulary to have indices of words
		for headline in headlines_annotated:
			headline = headline.split(' ')
			for word in headline:
                            if word not in headline:
			        vocab[word] = index
                                index += 1
                vector_length = len(vocab)
                for headline in headlines_annotated:
                    output = np.zeros((vector_length))
                    headline = headline.split(' ')
                    for word in headline:
                        if output[vocab[word]] == 0:
                            output[vocab[word]] = 1
                        else:
                            output[vocab[word]] += 1
                    # apply softmax
                    output = map(lambda x: e**x, output)
                    output = output / sum(output)
                    y.append(output)
                
                # create input x
                x = []
                v = DictVectorizer()
                for index, row in data.iterrows():
                    input = {}
                    for name in column:
                        input[name] = row[name]
                    x.append(input)
                x = v.fit_transform(x)
                
                self.vocab_size = len(vocab)
                self.is_trained = False
                return (x,y)
	
        def train(self, learning_rate = 0.01, epochs=20, batch_size=256):
            input_size = len(self.x[0])
            if not self.is_trained:
                model = Sequential()
                model.add(Dense(2*input_size,input_dim=input_size))
                model.add(Activation('relu'))
                model.add(Dropout(0.25))
                model.add(Dense(self.vocab_size))
                model.add(Activation('softmax'))
                sgd = SGD(lr=learning_rate)
                model.compile('mean_squared_error', optimizer=sgd)
                model.fit(self.xtrain, self.ytrain, nb_epoch = epochs, batch_size=batch_size)

                self.model = model
                self.is_trained = True
            else:
                print 'the model is already trained'
        
        def predict(self):
            if self.is_trained:
                print self.model.predict_classes(self.xtest)
                print self.model.predict_proba(self.xtest)
            else:
                print 'the model has not been trained'

e = Embedding()
