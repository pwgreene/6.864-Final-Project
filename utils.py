COLUMNS = [
        'game_year','game_week','team_1_abbr','team_1_city','team_1_mascot','team_1_score',
        'team_1_leader_passing','team_1_leader_passing_yds','team_1_leader_passing_td','team_1_leader_passing_int',
        'team_1_leader_rushing','team_1_leader_rushing_yds','team_1_leader_rushing_td','team_1_leader_receiving',
        'team_1_leader_receiving_yds','team_1_leader_receiving_td','team_2_abbr','team_2_city','team_2_mascot',
        'team_2_score','team_2_leader_passing','team_2_leader_passing_yds','team_2_leader_passing_td','team_2_leader_passing_int',
        'team_2_leader_rushing','team_2_leader_rushing_yds','team_2_leader_rushing_td','team_2_leader_receiving','team_2_leader_receiving_yds',
        'team_2_leader_receiving_td','game_leader_scorer','game_leader_scorer_points','game_leader_kicker','game_leader_kicker_points',
        'game_headline','game_headline_annotated','clean_data'
    ]

COLUMN_TO_INDEX = dict((COLUMNS[i], i) for i in range(len(COLUMNS)))

def extract_headlines(csvfile):
    """
    :param csvfile: a csv formatted file with columns labeled COLUMNS
    :return: the headlines (list(str))
    """

    data = pd.read_csv(csvfile, names=COLUMNS, sep=',',skiprows=[0])
    # only take headlines with clean data field marked as 1
    headlines = [data['game_headline_annotated'][i] for i in range(len(data['game_headline_annotated']))
                 if data['clean_data'][i]]
    return headlines

def create_vocabulary(headlines):
    """
    creates a vocabulary of all the words in headlines
    :param headlines: list(str)
    :return: a dict mapping each unique word to a unique index
    """
    vocab = {}
    for headline in headlines:
        headline = headline.split()
        for word in headline:
            word = clean_word(word)
            if word not in vocab:
                vocab[word] = len(vocab)
    return vocab

def clean_word(word):
    """
    remove trailing punctuation and makes lowercase. USE BEFORE ADDING TO VOCAB
    :param word: str
    :return: lowercase str without trailing punctuation
    """

    if word[-1] in ",.-_'":
        word = word[:-1]
    word = word.lower()
    return word

def substitute_values_in_headline(values, headline):
    """
    Substitute the values given in values (that correspond to COLUMNS) into the output headline
    example: [team_1] beats [team_2] becomes
    :param values:
    :param headline:
    :return:
    """
    pass #TODO

if __name__ == "__main__":
    sample_headlines = ["The President met with the man", "The world is now much hotter than last year"]
    print create_vocabulary(sample_headlines)