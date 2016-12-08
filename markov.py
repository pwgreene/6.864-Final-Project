import random
import numpy as np
from utils import clean_word

class MarkovChain:

    def __init__(self, data=None):
        self.start_state = "/^s"
        self.end_state = "/^e"
        self.words = {self.start_state:0, self.end_state:1}
        self.transitions = np.zeros((2,2)) #self.transtions[a][b] is the prob of transitioning from a to b (nested dictionary)
        self.add_transtion_count(self.end_state, self.end_state) #so probabilities sum to 1
        if data is not None:
            self.estimate_transition_probs(data)

    def estimate_transition_probs(self, data):
        """
        estimate transition parameters from data
        :param data: list of strings
        :return: None
        """

        for phrase in data:
            phrase_words = phrase.split()
            for i in range(len(phrase_words)):
                curr_word = clean_word(phrase_words[i])
                if curr_word not in self.words:
                    self.words[curr_word] = len(self.words)
                    self.expand_transition_array()
                if i == 0:
                    self.add_transtion_count(self.start_state, curr_word)
                elif i == len(phrase_words)-1:
                    self.add_transtion_count(curr_word, self.end_state)
                    break
                next_word = clean_word(phrase_words[i+1])
                if next_word not in self.words:
                    self.words[next_word] = len(self.words)
                    self.expand_transition_array()
                self.add_transtion_count(curr_word, next_word)

        for row in self.transitions:
            total = np.sum(row)
            if total != 0:
                row /= np.sum(row)

    def generate_sentence(self):
        word_list = [word for word in sorted(self.words.keys(), key=lambda x: self.words[x])]
        sentence = ""
        curr_state = self.words[self.start_state]
        transitions_probs = self.transitions[self.words[self.start_state]]
        while curr_state != self.words[self.end_state]:
            sentence += " "+word_list[curr_state]
            next_state = np.random.choice(range(len(self.words)), p=transitions_probs)
            transitions_probs = self.transitions[next_state]
            curr_state = next_state
        return sentence

    def apply_word_probabilites(self, word_to_prob):
        """
        each row of self.transitions becomes the (normalized) elem-wise product of that row and the cooresponding word
        probability vector created from a dictionary mapping each word to its corresponding probability
        :param word_to_prob: dict mapping each word in the vocab to its probability
        :return: None. Mutates self.transitions (a numpy array)
        """
        alpha = 10e-6
        prob_vector = np.zeros(len(self.words))
        for word in word_to_prob.keys():
            assert word in self.words #theres a problem if the input probabilites has a word never seen before
            prob_vector[self.words[word]] = word_to_prob[word] + alpha
        prob_vector[self.words[self.start_state]] = 1.0
        prob_vector[self.words[self.end_state]] = 1.0
        for i in range(len(self.transitions)):
            #print 'before', self.transitions[i]
            self.transitions[i] = self.transitions[i] * prob_vector
            #print np.linalg.norm(self.transitions[i])
            self.transitions[i] /= sum(self.transitions[i])
            #print self.transitions[i]


    def add_transtion_count(self, from_word, to_word):
        """
        increment number of transitions from from_word to to_word. Both words must be in self.words
        :return: None
        """
        self.transitions[self.words[from_word]][self.words[to_word]] += 1

    def expand_transition_array(self):
        self.transitions = np.column_stack([self.transitions, np.zeros((len(self.words)-1, 1))])
        self.transitions = np.vstack([self.transitions, np.zeros((1, len(self.words)))])

if __name__ == "__main__":
    #tests
    #test sentence generation
    data = ["Sally sells seashells by the seashore.", "Sally did not like the other man.", "The president met with the man."]
    markov = MarkovChain(data)
    # print markov.generate_sentence()
    word_prob = {}
    #test applying a probability vector
    for word in markov.words.keys():
        word_prob[word] = 1./len(markov.words)
    markov.apply_word_probabilites(word_prob)
    # print markov.transitions