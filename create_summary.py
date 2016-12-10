import embedding
import pandas as pd
import markov
from utils import prune

def bigram_summary():

    f = 'data/nfl_game_stats_2016_annotated_clean.csv'
    partition = 0.70
    e = embedding.Embedding(f,partition)
    e.train('categorical_crossentropy')
    classes, proba = e.predict()


    # print len(generator.words)
    e.normalize()
    keyword = e.norm
    #word_to_prob = e.word_to_prob()
    # for i in range(len(word_to_prob)):
    #     if i == 1:
    #         w_to_prob = sorted(word_to_prob[i].items(), key=lambda x: x[1])[-10:]
    #         print w_to_prob
    #         generator.apply_word_probabilites(word_to_prob[i])
    #         print generator.generate_sentence()
    for i in range(len(keyword)):
        data = prune(e.headlines_annotated, keyword[i])
        generator = markov.MarkovChain(data)
        # print proba_norm[i]
    # generator.apply_word_probabilites(word_to_prob)
    # print generator.generate_sentence()


def extract_headlines(csvfile):
    columns = [
        'game_year','game_week','team_1_abbr','team_1_city','team_1_mascot','team_1_score',
        'team_1_leader_passing','team_1_leader_passing_yds','team_1_leader_passing_td','team_1_leader_passing_int',
        'team_1_leader_rushing','team_1_leader_rushing_yds','team_1_leader_rushing_td','team_1_leader_receiving',
        'team_1_leader_receiving_yds','team_1_leader_receiving_td','team_2_abbr','team_2_city','team_2_mascot',
        'team_2_score','team_2_leader_passing','team_2_leader_passing_yds','team_2_leader_passing_td','team_2_leader_passing_int',
        'team_2_leader_rushing','team_2_leader_rushing_yds','team_2_leader_rushing_td','team_2_leader_receiving','team_2_leader_receiving_yds',
        'team_2_leader_receiving_td','game_leader_scorer','game_leader_scorer_points','game_leader_kicker','game_leader_kicker_points',
        'game_headline','game_headline_annotated','clean_data'
    ]
    data = pd.read_csv(csvfile, names=columns, sep=',',skiprows=[0])
    # only take headlines with clean data field marked as 1
    headlines = [data['game_headline_annotated'][i] for i in range(len(data['game_headline_annotated']))
                 if data['clean_data'][i]]
    print headlines
    return headlines

bigram_summary()