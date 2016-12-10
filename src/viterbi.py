import numpy as np

class Viterbi(object):

    def __init__(self, n_states, n_features, alpha=10e-6):
        self.n_states = n_states #number of defined states (doesn't include START and STOP)
        self.start_state = n_states
        self.stop_state = n_states+1
        self.n_emissions = 2**n_features
        self.a = np.zeros((n_states+2, n_states+2)) #a[u][v] is the prob of going from state u to v
        self.b = []
        self.alpha = alpha
        for state in range(n_states+2):
            self.b.append({})

    def train(self, data):
        """
        Estimate the model parameters, sets a and b. Must be run before predict
        :param data: a sequence of emissions in feature vector form
        :return: nothing
        """
        #estimate parameters with counts
        for sequence in data:
            for i in range(len(sequence)):
                emission = sequence[i][0]
                state = sequence[i][1]
                #create a
                if i == 0:
                    self.a[self.start_state][state] += 1.
                else:
                    previous_state = sequence[i-1][1]
                    self.a[previous_state][state] += 1.
                if i == len(sequence) - 1:
                    self.a[state][self.stop_state] += 1.
                #create b
                #emission_index = int("".join([str(int(x)) for x in emission]), 2)
                self.b[state][emission] = self.b[state].get(emission, 0) + 1

        #now normalize each probability
        for state in range(self.n_states):
            denom = np.sum(self.a[state])
            if not denom == 0:
                self.a[state] /= np.sum(self.a[state])
            denom = np.sum(self.b[state].values())
            if denom != 0:
                for key in self.b[state].keys():
                    self.b[state][key] /= float(denom)
        self.a[self.start_state] /= np.sum(self.a[self.start_state])

    def predict(self, data):
        """
        Predict the probability of sequences of tags and assigns the tags by running viterbi algorithm
        :param data: a seqence of emission in feature vector form
        :return: the tags of the highest probability sequence of tags
        """
        labels = []
        #add-alpha smoothing for words in the test data that aren't in the training data
        for sequence in data:
            for i in range(len(sequence)-1):
                emission = sequence[i][0]
                for state in range(self.n_states):
                    if emission not in self.b[state]:
                        self.b[state][emission] = self.alpha
        for state in range(self.n_states):
            denom = np.sum(self.b[state].values())
            if denom != 0:
                for key in self.b[state].keys():
                    self.b[state][key] /= float(denom)
        #VITERBI
        for sequence in data:
            #dynamic programming part
            pi = np.zeros((len(sequence)+2, self.n_states+2)) #index the sequence starting at zero
            pi[0][self.start_state] = 1.0 #base case
            for k in range(1, len(sequence)+1): #k = 1...n where n is length of the sequence
                x_k = sequence[k-1][0]
                for v in range(self.n_states+1):
                    for u in range(self.n_states+1):
                        pi[k][v] = max(pi[k][v], pi[k-1][u]*self.a[u][v]*(self.b[v].get(x_k, 0)))

            #backtracking part, iterate through backwards
            seq_labels = []
            last_label, max_val = None, 0
            for v in range(self.n_states+1):
                if pi[len(sequence)][v]*self.a[v][self.stop_state] >= max_val:
                    last_label, max_val = v, pi[len(sequence)][v]*self.a[v][self.stop_state]
            seq_labels.append(last_label)

            for n in range(1, len(sequence))[::-1]:
                best_u, max_val = None, 0
                for u in range(self.n_states+1):
                    argmax_val = pi[n][u]*self.a[u][last_label]
                    if argmax_val >= max_val:
                        max_val = argmax_val
                        best_u = u
                last_label = best_u
                seq_labels.append(best_u)
            labels.extend(seq_labels[::-1])
        return labels
