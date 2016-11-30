import twitter
import sys
from preprocess import run
import char
import test_char
import math

api = twitter.Api(consumer_key='xy8P84IZrXd2KvD0ZtLHLGDhg', consumer_secret='XQ9qpd0MHb2XZNhFmBQ4PWzNUwVMrWA82vTZm0ArwzKjhCbx2k', access_token_key='782844091449171968-Q7AxZ0nMPYYdbSuazJ2YrbChLl5adiZ', \
        access_token_secret='ecWdBWCZA3G8Er5OuS9jk5lujwqvVbPTjfK6Yie6bGAzq')

def get_tweets():
	users = open('verified_accounts_sn_nfl.txt', 'r').readlines()
	tweet_file = open('tweets.txt','w+')
	for user in users:
		tweet_objects = api.GetUserTimeline(screen_name=user)
		for t in tweet_objects:
			tweet_file.write(t.text.encode('utf-8') + '\n')
	tweet_file.close()

def preprocess(infile, outfile):
	run(infile,outfile)

def partition(file):
	percent_training = 0.70
	percent_validation = 0.20
	train = open('train.txt','w+')
	validation = open('validation.txt','w+')
	test = open('test.txt','w+')
	with open(file,'w+') as data:
		lines = data.readlines()
		training_lines = lines[:int(math.floor(len(lines)*percent_training))]
		train.writelines(training_lines)
		train.close()
		validation_lines = lines[int(math.floor(len(lines)*percent_training)):int(math.floor(len(lines)*(percent_training+percent_validation)))]
		validation.writelines(validation_lines)
		validation.close()
		test_lines = lines[int(math.floor(len(lines)*(percent_training+percent_validation))):]
		test.writelines(test_lines)
		test.close()

def train(outfile,val_path,save_path):
	char.main(outfile,val_path,save_path,num_epochs=10)

def test():
	test_char.main()
# we convert raw tweet text -> tokenized tweets
# train model, validate our encoder, and test

def main(args):

	# get_tweets()
	preprocess('tweets.txt','preprocess_tweets.txt')
	partition('preprocess_tweets.txt') # now we have train.txt, val.txt
	train('train.txt','validation.txt','/Users/jaclarke/Desktop/6.864-Final-Project/tweet2vec/model')
	#test()



if __name__ == '__main__':
	main(sys.argv)