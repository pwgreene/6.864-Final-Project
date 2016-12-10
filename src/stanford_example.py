from nltk.parse import stanford
from nltk.parse import generate
import os

parser = stanford.StanfordParser()
sentences = parser.raw_parse_sents(("game_leader_kicker makes game_leader_kicker_points field goals, helps team_1_mascot beat team_2_mascot game_score", "team_1_leader_passing accounts for team_1_leader_passing_td TDs, team_1_mascot beat team_2_mascot game_score"))

for line in sentences:
    for sentence in line:
        sentence.draw()
