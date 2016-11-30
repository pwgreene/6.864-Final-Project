import csv
import datetime
import twitter

class NFLGame:

    def __init__(self, visitor, home, time):
        self.home = home
        self.visitor = visitor
        self.time_start = time
        # self.time_end = time+
        self.score = (0,0)

    def set_score(self, home_score, visitor_score):
        self.score = (home_score, visitor_score)

    def set_time(self, time):
        self.time = time

    def __str__(self):
        return "%s @ %s on %s" % (self.visitor, self.home, self.time_start)


def extract_games(csvfile, year):
    games = []
    with open(csvfile) as gamefile:
        csvreader = csv.reader(gamefile)
        csvreader.next()
        for line in csvreader:
            gametime = datetime.datetime.strptime(("%s %s %s" % (line[4][:-2], line[5], year)).strip(),
                                                  "%B %d %I:%M %p %Z %Y")
            games.append(NFLGame(line[0], line[1][1:], gametime))
    return games

api = twitter.Api()

results = api.GetUserTimeline(screen_name='Parker_Greene', include_rts=False, exclude_replies=True)
for tweet in results:
    time = datetime.datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y")
    print time

# for game in  extract_games('nfl-2015-schedule.csv', 2015):
#     print game.time_start