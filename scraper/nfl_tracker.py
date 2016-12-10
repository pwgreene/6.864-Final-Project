from bs4 import BeautifulSoup
import urllib2
import csv
import sys

data_dict_team_city = {
	'BAL': 'Baltimore',
	'CIN': 'Cincinnati',
	'CLE': 'Cleveland',
	'PIT': 'Pittsburgh',
	'HOU': 'Houston',
	'IND': 'Indianapolis',
	'JAX': 'Jacksonville',
	'TEN': 'Tennessee',
	'CHI': 'Chicago',
	'DET': 'Detroit',
	'GB': 'Green Bay',
	'MIN': 'Minnesota',
	'ATL': 'Atlanta',
	'CAR': 'Carolina',
	'NO': 'New Orleans',
	'TB': 'Tampa Bay',
	'BUF': 'Buffalo',
	'MIA': 'Miami',
	'NE': 'New England',
	'NYJ': 'New York',
	'DEN': 'Denver',
	'KC': 'Kansas City',
	'OAK': 'Oakland',
	'SD': 'San Diego',
	'DAL': 'Dallas',
	'NYG': 'New York',
	'PHI': 'Philadelphia',
	'WSH': 'Washington',
	'ARI': 'Arizona',
	'STL': 'St. Louis',
	'SF': 'San Francisco',
	'SEA': 'Seattle',
	'LA': 'Los Angeles'
}

data_dict_team_mascot = {
	'BAL': 'Ravens',
	'CIN': 'Bengals',
	'CLE': 'Browns',
	'PIT': 'Steelers',
	'HOU': 'Texans',
	'IND': 'Colts',
	'JAX': 'Jaguars',
	'TEN': 'Titans',
	'CHI': 'Bears',
	'DET': 'Lions',
	'GB': 'Packers',
	'MIN': 'Vikings',
	'ATL': 'Falcons',
	'CAR': 'Panthers',
	'NO': 'Saints',
	'TB': 'Buccaneers',
	'BUF': 'Bills',
	'MIA': 'Dolphins',
	'NE': 'Patriots',
	'NYJ': 'Jets',
	'DEN': 'Broncos',
	'KC': 'Chiefs',
	'OAK': 'Raiders',
	'SD': 'Chargers',
	'DAL': 'Cowboys',
	'NYG': 'Giants',
	'PHI': 'Eagles',
	'WSH': 'Redskins',
	'ARI': 'Cardinals',
	'STL': 'Rams',
	'SF': '49ers',
	'SEA': 'Seahawks',
	'LA': 'Rams'
}

data_dict_team_coach = {
	'BAL': 'John Harbaugh',
	'CIN': 'Marvin Lewis',
	'CLE': 'Mike Pettine',
	'PIT': 'Mike Tomlin',
	'HOU': "Bill O'brien",
	'IND': 'Chuck Pagano',
	'JAX': 'Gus Bradley',
	'TEN': 'Ken Whisenhunt',
	'CHI': 'John Fox',
	'DET': 'Jim Caldwell',
	'GB': 'Mike McCarthy',
	'MIN': 'Mike Zimmer',
	'ATL': 'Dan Quinn',
	'CAR': 'Ron Rivera',
	'NO': 'Sean Payton',
	'TB': 'Lovie Smith',
	'BUF': 'Rex Ryan',
	'MIA': 'Joe Philbin',
	'NE': 'Bill Belichick',
	'NYJ': 'Todd Bowles',
	'DEN': 'Gary Kubiak',
	'KC': 'Andy Reid',
	'OAK': 'Jack Del Rio',
	'SD': 'Mike McCoy',
	'DAL': 'Jason Garrett',
	'NYG': 'Tom Coughlin',
	'PHI': 'Chip Kelly',
	'WSH': 'Jay Gruden',
	'ARI': 'Bruce Arians',
	'STL': 'Jeff Fisher',
	'SF': 'Jim Tomsula',
	'SEA': 'Pete Carroll',
	'LA': 'Jeff Fisher'
}

data_dict_team_league = {
	'BAL': 'AFC',
	'CIN': 'AFC',
	'CLE': 'AFC',
	'PIT': 'AFC',
	'HOU': 'AFC',
	'IND': 'AFC',
	'JAX': 'AFC',
	'TEN': 'AFC',
	'CHI': 'NFC',
	'DET': 'NFC',
	'GB': 'NFC',
	'MIN': 'NFC',
	'ATL': 'NFC',
	'CAR': 'NFC',
	'NO': 'NFC',
	'TB': 'NFC',
	'BUF': 'AFC',
	'MIA': 'AFC',
	'NE': 'AFC',
	'NYJ': 'AFC',
	'DEN': 'AFC',
	'KC': 'AFC',
	'OAK': 'AFC',
	'SD': 'AFC',
	'DAL': 'NFC',
	'NYG': 'NFC',
	'PHI': 'NFC',
	'WSH': 'NFC',
	'ARI': 'NFC',
	'STL': 'NFC',
	'SF': 'NFC',
	'SEA': 'NFC',
	'LA': 'NFC'
}

data_dict_team_division = {
	'BAL': 'North',
	'CIN': 'North',
	'CLE': 'North',
	'PIT': 'North',
	'HOU': 'South',
	'IND': 'South',
	'JAX': 'South',
	'TEN': 'South',
	'CHI': 'North',
	'DET': 'North',
	'GB': 'North',
	'MIN': 'North',
	'ATL': 'South',
	'CAR': 'South',
	'NO': 'South',
	'TB': 'South',
	'BUF': 'East',
	'MIA': 'East',
	'NE': 'East',
	'NYJ': 'East',
	'DEN': 'West',
	'KC': 'West',
	'OAK': 'West',
	'SD': 'West',
	'DAL': 'East',
	'NYG': 'East',
	'PHI': 'East',
	'WSH': 'East',
	'ARI': 'West',
	'STL': 'West',
	'SF': 'West',
	'SEA': 'West',
	'LA': 'West'
}

data_game_year = []
data_game_week = []

data_teams = []
data_scores = []
data_headlines = []
data_blurbs = []
data_leader_passer = []
data_leader_rusher = []
data_leader_receiver = []
data_leader_scorer = []
data_leader_kicker = []

year_max = 2016
week_max = 17

for index_year in xrange(2016, year_max + 1, 1):
	for index_week in xrange(1, week_max + 1, 1):

		url_response = urllib2.urlopen("http://www.espn.com/nfl/schedule/_/year/" + str(index_year) + "/week/" + str(index_week))
		html_response = url_response.read()

		soup = BeautifulSoup(html_response)
		list_game_teams = soup.find_all("a", {"name": "&lpos=nfl:schedule:team", "class": "team-name"})
		list_game_scores = soup.find_all("a", {"name": "&lpos=nfl:schedule:score"})
		

		# get teams and score data
		data_teams_temp = []
		data_scores_temp = []
		for i in list_game_scores:
			score_tokens = i.contents[0].split(' ')
			if len(score_tokens) >= 4:
				print score_tokens[0]
				data_scores_temp.append([score_tokens[1][:-1], score_tokens[3]])
				data_teams_temp.append([score_tokens[0], score_tokens[2], data_dict_team_city[score_tokens[0]], data_dict_team_city[score_tokens[2]], data_dict_team_mascot[score_tokens[0]], data_dict_team_mascot[score_tokens[2]], data_dict_team_coach[score_tokens[0]], data_dict_team_coach[score_tokens[2]]])
				data_game_year.append(index_year)
				data_game_week.append(index_week)

		# get headline and blurb data
		data_headlines_temp = []
		data_blurbs_temp = []

		# get leader data
		data_leader_passer_temp = []
		data_leader_rusher_temp = []
		data_leader_receiver_temp = []
		data_leader_scorer_temp = []
		data_leader_kicker_temp = []

		for i in list_game_scores:
			hyperlink_endpoint = i['href']
			print str(index_year) + " " + str(index_week) + " " + str(hyperlink_endpoint)
			url_crawl_response = urllib2.urlopen("http://www.espn.com" + hyperlink_endpoint)
			html_crawl_response = url_crawl_response.read()

			crawl_soup = BeautifulSoup(html_crawl_response)
			list_game_headline = crawl_soup.find_all("a", {"name": "&lpos=:editorial"})

			for j in list_game_headline:
				data_headlines_temp.append(j.contents[0])

			list_game_blurb = crawl_soup.find_all("p", {"data-behavior": "linkable"})
			for j in list_game_blurb:
				data_blurbs_temp.append(j.contents[0])


			list_game_leaders_away = crawl_soup.find_all("div", {"class": "away-leader"})
			for j in xrange(len(list_game_leaders_away)):
				crawl_soup_temp = BeautifulSoup(str(list_game_leaders_away[j]))
				player_name_list = "N/A"
				try:
					player_name_list = crawl_soup_temp.find("span", {"class": "player-name"})["title"]
				except:
					pass
				player_team_list = crawl_soup_temp.find("span", {"class": "player-team"}).contents
				player_stat_list = crawl_soup_temp.find("span", {"class": "player-stats"}).contents
				#print player_name_list + " " + str(player_stat_list) + "\n"


				# 1st - passing, 2nd - rushing, 3rd - receiving
				if j == 0:
					stat_dict = {'YDS': 0, 'TD': 0, 'INT': 0}

					for k in str(player_stat_list[0]).split(','):
						if 'YDS' in k:
							stat_dict['YDS'] = k[1:-9]
						elif 'TD' in k:
							stat_dict['TD'] = k[1:-8]
						elif 'INT' in k:
							stat_dict['INT'] = k[1:-9]

					data_leader_passer_temp.append([str(player_team_list[0]), str(player_name_list), str(stat_dict['YDS']), str(stat_dict['TD']), str(stat_dict['INT'])])
					
				if j == 1:
					stat_dict = {'YDS': 0, 'TD': 0}

					for k in str(player_stat_list[0]).split(','):
						if 'YDS' in k:
							stat_dict['YDS'] = k[1:-9]
						elif 'TD' in k:
							stat_dict['TD'] = k[1:-8]

					data_leader_rusher_temp.append([str(player_team_list[0]), str(player_name_list), str(stat_dict['YDS']), str(stat_dict['TD'])])

				if j == 2:
					stat_dict = {'YDS': 0, 'TD': 0}

					for k in str(player_stat_list[0]).split(','):
						if 'YDS' in k:
							stat_dict['YDS'] = k[1:-9]
						elif 'TD' in k:
							stat_dict['TD'] = k[1:-8]

					data_leader_receiver_temp.append([str(player_team_list[0]), str(player_name_list), str(stat_dict['YDS']), str(stat_dict['TD'])])

			list_game_leaders_home = crawl_soup.find_all("div", {"class": "home-leader"})
			for j in xrange(len(list_game_leaders_home)):
				crawl_soup_temp = BeautifulSoup(str(list_game_leaders_home[j]))
				player_name_list = "N/A"
				try:
					player_name_list = crawl_soup_temp.find("span", {"class": "player-name"})["title"]
				except:
					pass
				player_team_list = crawl_soup_temp.find("span", {"class": "player-team"}).contents
				player_stat_list = crawl_soup_temp.find("span", {"class": "player-stats"}).contents

				
				#print player_name_list + " " + str(player_stat_list) + "\n"

				# 1st - passing, 2nd - rushing, 3rd - receiving
				if j == 0:
					stat_dict = {'YDS': 0, 'TD': 0, 'INT': 0}

					for k in player_stat_list[0].split(','):
						if 'YDS' in k:
							stat_dict['YDS'] = k[1:-4]
						elif 'TD' in k:
							stat_dict['TD'] = k[1:-3]
						elif 'INT' in k:
							stat_dict['INT'] = k[1:-4]

					data_leader_passer_temp.append([str(player_team_list[0]), str(player_name_list), str(stat_dict['YDS']), str(stat_dict['TD']), str(stat_dict['INT'])])
					
				if j == 1:
					stat_dict = {'YDS': 0, 'TD': 0}

					for k in player_stat_list[0].split(','):
						if 'YDS' in k:
							stat_dict['YDS'] = k[1:-4]
						elif 'TD' in k:
							stat_dict['TD'] = k[1:-3]

					data_leader_rusher_temp.append([str(player_team_list[0]), str(player_name_list), str(stat_dict['YDS']), str(stat_dict['TD'])])

				if j == 2:
					stat_dict = {'YDS': 0, 'TD': 0}

					for k in player_stat_list[0].split(','):
						if 'YDS' in k:
							stat_dict['YDS'] = k[1:-4]
						elif 'TD' in k:
							stat_dict['TD'] = k[1:-3]

					data_leader_receiver_temp.append([str(player_team_list[0]), str(player_name_list), str(stat_dict['YDS']), str(stat_dict['TD'])])


			player_scoring_dict_td = {}
			player_scoring_dict_fg = {}
			player_drives_list = crawl_soup.find_all("td", {"class": "game-details"})
			for j in player_drives_list:
				crawl_soup_temp = BeautifulSoup(str(j.contents[0]))

				if len(crawl_soup_temp.find("div", {"class": "score-type"}).contents) > 0:
					scoring_drive_type = crawl_soup_temp.find("div", {"class": "score-type"}).contents[0]
					#scoring_drive_time = crawl_soup_temp.find("div", {"class": "time-stamp"}).contents[0]

					scoring_drive_desc = crawl_soup_temp.find("div", {"class": "headline"})
					if len(scoring_drive_desc) > 0:
						scoring_drive_desc = scoring_drive_desc.contents[0].split(' ')
						if len(scoring_drive_desc) > 3:
							player_name = scoring_drive_desc[0] + " " + scoring_drive_desc[1]

							if str(scoring_drive_type) == "TD":
								if player_name in player_scoring_dict_td:
									player_scoring_dict_td[player_name] = player_scoring_dict_td[player_name] + 1
								else:
									player_scoring_dict_td[player_name] = 1

							if str(scoring_drive_type) == "FG":
								if player_name in player_scoring_dict_fg:
									player_scoring_dict_fg[player_name] = player_scoring_dict_fg[player_name] + 1
								else:
									player_scoring_dict_fg[player_name] = 1
							#print str(scoring_drive_time) + " " + str(scoring_drive_type) + " " + str(scoring_drive_desc) 

			temp_var_leading_scorer_name = "N/A"
			temp_var_leading_scorer_score = 0

			for scorer in player_scoring_dict_td:
				if player_scoring_dict_td[scorer] > temp_var_leading_scorer_score:
					temp_var_leading_scorer_name = scorer
					temp_var_leading_scorer_score = player_scoring_dict_td[scorer]
		
			data_leader_scorer_temp.append([temp_var_leading_scorer_name, temp_var_leading_scorer_score])

			temp_var_leading_kicker_name = "N/A"
			temp_var_leading_kicker_score = 0

			for scorer in player_scoring_dict_fg:
				if player_scoring_dict_fg[scorer] > temp_var_leading_kicker_score:
					temp_var_leading_kicker_name = scorer
					temp_var_leading_kicker_score = player_scoring_dict_fg[scorer]
		
			data_leader_kicker_temp.append([temp_var_leading_kicker_name, temp_var_leading_kicker_score])



		data_teams.extend(data_teams_temp)
		data_scores.extend(data_scores_temp)
		data_headlines.extend(data_headlines_temp)
		data_blurbs.extend(data_blurbs_temp)
		data_leader_passer.extend(data_leader_passer_temp)
		data_leader_rusher.extend(data_leader_rusher_temp)
		data_leader_receiver.extend(data_leader_receiver_temp)
		data_leader_scorer.extend(data_leader_scorer_temp)
		data_leader_kicker.extend(data_leader_kicker_temp)

# # configure string
index_teams = 0
index_scores = 0
index_players = 0
index_yardage = 0

f = open("nfl_game_stats_2016.csv", 'wt')

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
		"game_headline"))

	print len(data_game_year)
	print len(data_teams)
	print len(data_leader_passer)
 	for i in xrange(0, len(data_teams), 1):
 		row_data = ()
 		print data_teams[i][0]
 		print i
 		print len(data_leader_passer)
 		print data_leader_passer[i * 2][1]
 		if data_teams[i][0] == data_leader_passer[i * 2][0]:
	 		row_data = (str(data_game_year[i]), str(data_game_week[i]),
	 			str(data_teams[i][0]), data_dict_team_city[str(data_teams[i][0])], data_dict_team_mascot[str(data_teams[i][0])], str(data_scores[i][0]),
	 			str(data_leader_passer[i * 2][1]), str(data_leader_passer[i * 2][2]), str(data_leader_passer[i * 2][3]), str(data_leader_passer[i * 2][4]),
	 			str(data_leader_rusher[i * 2][1]), str(data_leader_rusher[i * 2][2]), str(data_leader_rusher[i * 2][3]),
	 			str(data_leader_receiver[i * 2][1]), str(data_leader_receiver[i * 2][2]), str(data_leader_receiver[i * 2][3]),
	 			str(data_teams[i][1]), data_dict_team_city[str(data_teams[i][1])], data_dict_team_mascot[str(data_teams[i][1])], str(data_scores[i][1]),
	 			str(data_leader_passer[i * 2 + 1][1]), str(data_leader_passer[i * 2 + 1][2]), str(data_leader_passer[i * 2 + 1][3]), str(data_leader_passer[i * 2 + 1][4]),
	 			str(data_leader_rusher[i * 2 + 1][1]), str(data_leader_rusher[i * 2 + 1][2]), str(data_leader_rusher[i * 2 + 1][3]),
	 			str(data_leader_receiver[i * 2 + 1][1]), str(data_leader_receiver[i * 2 + 1][2]), str(data_leader_receiver[i * 2 + 1][3]),
	 			str(data_leader_scorer[i][0]), str(data_leader_scorer[i][1]), str(data_leader_kicker[i][0]), str(data_leader_kicker[i][1]),
	 			str(data_headlines[i]))
	 	else:
	 		row_data = (str(data_game_year[i]), str(data_game_week[i]),
	 			str(data_teams[i][0]), data_dict_team_city[str(data_teams[i][0])], data_dict_team_mascot[str(data_teams[i][0])], str(data_scores[i][0]),
	 			str(data_leader_passer[i * 2 + 1][1]), str(data_leader_passer[i * 2 + 1][2]), str(data_leader_passer[i * 2 + 1][3]), str(data_leader_passer[i * 2 + 1][4]),
	 			str(data_leader_rusher[i * 2 + 1][1]), str(data_leader_rusher[i * 2 + 1][2]), str(data_leader_rusher[i * 2 + 1][3]),
	 			str(data_leader_receiver[i * 2 + 1][1]), str(data_leader_receiver[i * 2 + 1][2]), str(data_leader_receiver[i * 2 + 1][3]),
	 			str(data_teams[i][1]), data_dict_team_city[str(data_teams[i][1])], data_dict_team_mascot[str(data_teams[i][1])], str(data_scores[i][1]),
	 			str(data_leader_passer[i * 2][1]), str(data_leader_passer[i * 2][2]), str(data_leader_passer[i * 2][3]), str(data_leader_passer[i * 2][4]),
	 			str(data_leader_rusher[i * 2][1]), str(data_leader_rusher[i * 2][2]), str(data_leader_rusher[i * 2][3]),
	 			str(data_leader_receiver[i * 2][1]), str(data_leader_receiver[i * 2][2]), str(data_leader_receiver[i * 2][3]),
	 			str(data_leader_scorer[i][0]), str(data_leader_scorer[i][1]), str(data_leader_kicker[i][0]), str(data_leader_kicker[i][1]),
	 			str(data_headlines[i]))

 		writer.writerow(row_data)
finally:
 	f.close()


