import csv

filename = "nfl_game_stats_2016.csv"

annotated_headlines = []

with open(filename) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:

		# get current headline in db
		headline = row["game_headline"]

		############################################################################
		### REPLACE "team_1_city"
		############################################################################
		
		team_1_city = row["team_1_city"]

		# try to replace qb name alternates
		if team_1_city in headline:
			headline = headline[0:headline.index(team_1_city)] + "[team_1_city]" + headline[headline.index(team_1_city) + len(team_1_city):]

		############################################################################
		### REPLACE "team_2_city"
		############################################################################
		
		team_2_city = row["team_2_city"]

		# try to replace qb name alternates
		if team_2_city in headline:
			headline = headline[0:headline.index(team_2_city)] + "[team_2_city]" + headline[headline.index(team_2_city) + len(team_2_city):]

		############################################################################
		### REPLACE "team_1_abbr"
		############################################################################
		
		team_1_abbr = row["team_1_abbr"]

		# try to replace qb name alternates
		if team_1_abbr in headline:
			headline = headline[0:headline.index(team_1_abbr)] + "[team_1_abbr]" + headline[headline.index(team_1_abbr) + len(team_1_abbr):]

		############################################################################
		### REPLACE "team_2_abbr"
		############################################################################
		
		team_2_abbr = row["team_2_abbr"]

		# try to replace qb name alternates
		if team_2_abbr in headline:
			headline = headline[0:headline.index(team_2_abbr)] + "[team_2_abbr]" + headline[headline.index(team_2_abbr) + len(team_2_abbr):]

		############################################################################
		### REPLACE "team_1_mascot"
		############################################################################
		
		team_1_mascot = row["team_1_mascot"]

		# try to replace qb name alternates
		if team_1_mascot in headline:
			headline = headline[0:headline.index(team_1_mascot)] + "[team_1_mascot]" + headline[headline.index(team_1_mascot) + len(team_1_mascot):]

		############################################################################
		### REPLACE "team_2_mascot"
		############################################################################
		
		team_2_mascot = row["team_2_mascot"]

		# try to replace qb name alternates
		if team_2_mascot in headline:
			headline = headline[0:headline.index(team_2_mascot)] + "[team_2_mascot]" + headline[headline.index(team_2_mascot) + len(team_2_mascot):]

		############################################################################
		### REPLACE "team_1_score" + "-" + "team_2_score"
		############################################################################
		
		game_score = row["team_1_score"] + "-" + row["team_2_score"]

		# try to replace qb name alternates
		if game_score in headline:
			headline = headline[0:headline.index(game_score)] + "[game_score]" + headline[headline.index(game_score) + len(game_score):]
			
		############################################################################
		### REPLACE "team_1_leader_passing"
		############################################################################

		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		team_1_leader_passing = row["team_1_leader_passing"]
		team_1_leader_passing_tokens = team_1_leader_passing.split(' ')
		team_1_leader_passing_alternates = [team_1_leader_passing, team_1_leader_passing_tokens[0][0] + ". " + team_1_leader_passing_tokens[-1], team_1_leader_passing_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in team_1_leader_passing_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[team_1_leader_passing]" + headline[headline.index(name_alt) + len(name_alt):]

		############################################################################
		### REPLACE "team_2_leader_passing"
		############################################################################
		
		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		team_2_leader_passing = row["team_2_leader_passing"]
		team_2_leader_passing_tokens = team_2_leader_passing.split(' ')
		team_2_leader_passing_alternates = [team_2_leader_passing, team_2_leader_passing_tokens[0][0] + ". " + team_2_leader_passing_tokens[-1], team_2_leader_passing_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in team_2_leader_passing_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[team_2_leader_passing]" + headline[headline.index(name_alt) + len(name_alt):]

		############################################################################
		### REPLACE "game_leader_scorer"
		############################################################################

		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		game_leader_scorer = row["game_leader_scorer"]
		game_leader_scorer_tokens = game_leader_scorer.split(' ')
		game_leader_scorer_alternates = [game_leader_scorer, game_leader_scorer_tokens[0][0] + ". " + game_leader_scorer_tokens[-1], game_leader_scorer_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in game_leader_scorer_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[game_leader_scorer]" + headline[headline.index(name_alt) + len(name_alt):]

		############################################################################
		### REPLACE "game_leader_kicker"
		############################################################################
		
		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		game_leader_kicker = row["game_leader_kicker"]
		game_leader_kicker_tokens = game_leader_kicker.split(' ')
		game_leader_kicker_alternates = [game_leader_kicker, game_leader_kicker_tokens[0][0] + ". " + game_leader_kicker_tokens[-1], game_leader_kicker_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in game_leader_kicker_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[game_leader_kicker]" + headline[headline.index(name_alt) + len(name_alt):]

		############################################################################
		### REPLACE "team_1_leader_rushing"
		############################################################################
		
		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		team_1_leader_rushing = row["team_1_leader_rushing"]
		team_1_leader_rushing_tokens = team_1_leader_rushing.split(' ')
		team_1_leader_rushing_alternates = [team_1_leader_rushing, team_1_leader_rushing_tokens[0][0] + ". " + team_1_leader_rushing_tokens[-1], team_1_leader_rushing_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in team_1_leader_rushing_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[team_1_leader_rushing]" + headline[headline.index(name_alt) + len(name_alt):]

		############################################################################
		### REPLACE "team_2_leader_rushing"
		############################################################################
		
		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		team_2_leader_rushing = row["team_2_leader_rushing"]
		team_2_leader_rushing_tokens = team_2_leader_rushing.split(' ')
		team_2_leader_rushing_alternates = [team_2_leader_rushing, team_2_leader_rushing_tokens[0][0] + ". " + team_2_leader_rushing_tokens[-1], team_2_leader_rushing_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in team_2_leader_rushing_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[team_2_leader_rushing]" + headline[headline.index(name_alt) + len(name_alt):]

		############################################################################
		### REPLACE "team_1_leader_receiving"
		############################################################################
		
		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		team_1_leader_receiving = row["team_1_leader_receiving"]
		team_1_leader_receiving_tokens = team_1_leader_receiving.split(' ')
		team_1_leader_receiving_alternates = [team_1_leader_receiving, team_1_leader_receiving_tokens[0][0] + ". " + team_1_leader_receiving_tokens[-1], team_1_leader_receiving_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in team_1_leader_receiving_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[team_1_leader_receiving]" + headline[headline.index(name_alt) + len(name_alt):]

		############################################################################
		### REPLACE "team_2_leader_rushing"
		############################################################################
		
		# create qb name alternates (Tom Brady -> ["Tom Brady", "T. Brady", "Brady"])
		team_2_leader_receiving = row["team_2_leader_receiving"]
		team_2_leader_receiving_tokens = team_2_leader_receiving.split(' ')
		team_2_leader_receiving_alternates = [team_2_leader_receiving, team_2_leader_receiving_tokens[0][0] + ". " + team_2_leader_receiving_tokens[-1], team_2_leader_receiving_tokens[-1]]

		# try to replace qb name alternates
		for name_alt in team_2_leader_receiving_alternates:
			if name_alt in headline:
				headline = headline[0:headline.index(name_alt)] + "[team_2_leader_receiving]" + headline[headline.index(name_alt) + len(name_alt):]


		# add annotated_headline to list of annotated headlines
		annotated_headlines.append(headline)


row_headers = [
	"game_year", "game_week",
		"team_1_abbr", "team_1_city", "team_1_mascot", "team_1_score",
		"team_1_leader_passing", "team_1_leader_passing_yds", "team_1_leader_passing_td", "team_1_leader_passing_int",
		"team_1_leader_rushing", "team_1_leader_rushing_yds", "team_1_leader_rushing_td",
		"team_1_leader_receiving", "team_1_leader_receiving_yds", "team_1_leader_receiving_td",
		"team_2_abbr", "team_2_city", "team_2_mascot", "team_2_score",
		"team_2_leader_passing", "team_2_leader_passing_yds", "team_2_leader_passing_td", "team_2_leader_passing_int",
		"team_2_leader_rushing", "team_2_leader_rushing_yds", "team_2_leader_rushing_td",
		"team_2_leader_receiving", "team_2_leader_receiving_yds", "team_2_leader_receiving_td",
		"game_leader_scorer", "game_leader_scorer_points", "game_leader_kicker", "game_leader_kicker_points",
		"game_headline"
]

f = open(filename[:-4] + "_annotated.csv", 'wt')


try:
	writer = csv.writer(f)
	writer.writerow(("game_year", "game_week",
		"team_1_abbr", "team_1_city", "team_1_mascot", "team_1_score",
		"team_1_leader_passing", "team_1_leader_passing_yds", "team_1_leader_passing_td", "team_1_leader_passing_int",
		"team_1_leader_rushing", "team_1_leader_rushing_yds", "team_1_leader_rushing_td",
		"team_1_leader_receiving", "team_1_leader_receiving_yds", "team_1_leader_receiving_td",
		"team_2_abbr", "team_2_city", "team_2_mascot", "team_2_score",
		"team_2_leader_passing", "team_2_leader_passing_yds", "team_2_leader_passing_td", "team_2_leader_passing_int",
		"team_2_leader_rushing", "team_2_leader_rushing_yds", "team_2_leader_rushing_td",
		"team_2_leader_receiving", "team_2_leader_receiving_yds", "team_2_leader_receiving_td",
		"game_leader_scorer", "game_leader_scorer_points", "game_leader_kicker", "game_leader_kicker_points",
		"game_headline", "game_headline_annotated"))

	
	with open(filename) as csvfile_followup:
		reader_followup = csv.DictReader(csvfile_followup)
		i = 0
		for row in reader_followup:
			row_data = (str(row["game_year"]), str(row["game_week"]),
				str(row["team_1_abbr"]), str(row["team_1_city"]), str(row["team_1_mascot"]), str(row["team_1_score"]),
				str(row["team_1_leader_passing"]), str(row["team_1_leader_passing_yds"]), str(row["team_1_leader_passing_td"]), str(row["team_1_leader_passing_int"]),
				str(row["team_1_leader_rushing"]), str(row["team_1_leader_rushing_yds"]), str(row["team_1_leader_rushing_td"]),
				str(row["team_1_leader_receiving"]), str(row["team_1_leader_receiving_yds"]), str(row["team_1_leader_receiving_td"]),
				str(row["team_2_abbr"]), str(row["team_2_city"]), str(row["team_2_mascot"]), str(row["team_2_score"]),
				str(row["team_2_leader_passing"]), str(row["team_2_leader_passing_yds"]), str(row["team_2_leader_passing_td"]), str(row["team_2_leader_passing_int"]),
				str(row["team_2_leader_rushing"]), str(row["team_2_leader_rushing_yds"]), str(row["team_2_leader_rushing_td"]),
				str(row["team_2_leader_receiving"]), str(row["team_2_leader_receiving_yds"]), str(row["team_2_leader_receiving_td"]),
				str(row["game_leader_scorer"]), str(row["game_leader_scorer_points"]), str(row["game_leader_kicker"]), str(row["game_leader_kicker_points"]),
				str(row["game_headline"]), str(annotated_headlines[i]))

			i = i + 1
 			writer.writerow(row_data)
finally:
 	f.close()

