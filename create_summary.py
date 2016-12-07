import embedding
import pandas as pd
import markov

def bigram_summary():
    f = 'nfl_game_stats_2016_annotated_clean.csv'
    partition = 0.70
    e = embedding.Embedding(f,partition)
    e.train('categorical_crossentropy')
    classes, proba = e.predict()
    proba_norm = e.normalize(proba)
    headlines = extract_headlines(f)
    generator = markov.MarkovChain(headlines)
    word_to_prob = {} #TODO: create word to probability dictionary
    generator.apply_word_probabilites(word_to_prob)
    print generator.generate_sentence()


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
    headlines = list(data['game_headline_annotated'])
    return headlines