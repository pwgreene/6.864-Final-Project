import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from math import exp, floor

class Embedding(object):

        def __init__(self,data_file,train_partition):
		
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
                            if word not in vocab:
			        vocab[word] = index
                                index += 1
		self.set_vocab(vocab)
                vector_length = len(vocab)
	   	self.vocab_size = vector_length
                for headline in headlines_annotated:
                    output = np.zeros((vector_length))
                    headline = headline.split(' ')
                    for word in headline:
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
                    inp = {}
                    for name in columns:
                        inp[name] = row[name]
                    x.append(inp)
                x = v.fit_transform(x).toarray()
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
		return (classes,proba)
	
	def normalize(self,predictions):
		norm = []
		for p in predictions:
			avg = np.average(p)
			norm.append(map(lambda x: x if x >= avg else 0, p))
		norm = np.array(norm)
		return norm



f = 'nfl_game_stats_2016_annotated_clean.csv'
partition = 0.70
e = Embedding(f,partition)
e.train('categorical_crossentropy')
classes, proba = e.predict()
proba_norm = e.normalize(proba)
for p in proba_norm:
	print p
