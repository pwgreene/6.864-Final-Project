import re
import pandas as pd

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

STATS_COLUMNS = [
        'team_1_score', 'team_1_leader_passing_yds','team_1_leader_passing_td','team_1_leader_passing_int', 'team_1_leader_rushing_yds',
        'team_1_leader_rushing_td','team_1_leader_receiving_yds','team_1_leader_receiving_td', 'team_2_score','team_2_leader_passing_yds',
        'team_2_leader_passing_td','team_2_leader_passing_int', 'team_2_leader_rushing_yds','team_2_leader_rushing_td','team_2_leader_receiving_yds',
        'team_2_leader_receiving_td','game_leader_scorer_points','game_leader_kicker_points', 'team_score_diff'
    ]

COLUMN_TO_INDEX = dict((COLUMNS[i], i) for i in range(len(COLUMNS)))
START_SYMBOL = "$"
END_SYMBOL = "@"
START_WORD = "/^s"
END_WORD = "/^e"

def keywords():
    keywords = []
    for keyword in COLUMNS:
        keywords.append('[' + keyword + ']')
    return keywords

def extract_column(csvfile, column=None):
    """
    :param csvfile: either a single csv file or list of files formatted with columns labeled COLUMNS
    :return: the headlines (list(str))
    """
    output_data = []
    for f in csvfile:
        data = pd.read_csv(csvfile, names=COLUMNS, sep=',',skiprows=[0])
        # only take headlines with clean data field marked as 1
        column_data = [data[column][i] for i in range(len(data[column]))
                     if data['clean_data'][i]]
        output_data.extend(column_data)

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

def create_char_vocabulary(headlines):
    """
    same as create_vocabulary except vocab is characters instead of words
    :param headlines: list(str) of headlines
    :return: dict{str:int} a dictionary mapping unique character to a unique int
    """
    headline_str = " ".join(headlines)
    chars = sorted(list(set(headline_str)))
    return dict((char, i) for i, char in enumerate(chars))

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
    example: /^s [team_1] beats [team_2] becomes Steelers beat Patriots.
    :param values: a list of values that correspond to COLUMNS
    :param headline: a string as output from sentence generator
    :return: a valid sentence created from headline and values
    """
    pattern = "\[(.*)\]"
    headline_as_list = headline.split()[1:] #ignore start
    new_headline = []
    for word in headline_as_list:
        match = re.match(pattern, word)
        if match:
            column = match.group(1)
            new_headline.append(values[COLUMN_TO_INDEX[column]])
        else:
            new_headline.append(word)
    return " ".join(new_headline)

def strat(val, ranges):
    """
    :param val a float of int value
    :param ranges an array of float or int values
    :return index i is val is numerically greater than or equal to but less than numbers at indices i and i+1
    """
    for i in range(1,len(ranges)):
        lo, hi = ranges[i-1], ranges[i]
        if val > lo and val <= hi:
            return i-1
    return len(ranges)-1

def prune(keywords, data):
    KEYWORDS = keywords()

    kw = []
    for i in range(keywords):
        if keywords[i] == 1:
            kw.append(KEYWORDS[i])
    sentences = []
    for p in data:
        for word in kw:
            # get smarter about combinations
            if word in p:
                sentences.append(p)
                break
    return sentences
            

if __name__ == "__main__":
    sample_headlines = ["The President met with the man", "The world is now much hotter than last year"]
    print create_vocabulary(sample_headlines)

    sample_headline = "/^s [team_1_mascot] beat [team_2_mascot]"
    sample_values = ["null" for i in range(len(COLUMNS))]
    sample_values[COLUMN_TO_INDEX["team_1_mascot"]] = "Steelers"
    sample_values[COLUMN_TO_INDEX["team_2_mascot"]] = "Patriots"
    print substitute_values_in_headline(sample_values, sample_headline)