import csv
import numpy as np

import urllib.request as urllib2
from bs4 import BeautifulSoup

import pandas as pd

data = []
data.append(('League', 'Score', 'Home Goals', 'Away Goals', 'Number of Matches'))

league = []
scores = []
hgs = []
ags = []
num_matches = [] 

# all pages to be scraped
country_urls = ['england', 'germany', 'spain', 'italy', 'france', 'portugal']

for country_url in country_urls:
	page = urllib2.urlopen('https://www.soccerstats.com/latest.asp?league=' + country_url + '_2018')
	soup = BeautifulSoup(page, 'html.parser')

	# get league name
	league_name = soup.find('h1').text.strip()

	table = soup.find('table', attrs={'bgcolor': '#cccccc'})
	sets = table.find_all('tr', attrs={'bgcolor': True})
	for item in sets:
		score_table = item.td

		# get scoreline
		score = score_table.b.text.strip()

		# parse string to get home and away goals
		if len(score) == 5:
			home_goals = int(score[0])
			away_goals = int(score[4])
		else:
			home_goals = np.nan
			away_goals = np.nan

		# get number of matches
		matches = score_table.find_next_sibling().text.strip()

		league.append(league_name)
		scores.append(score)
		hgs.append(home_goals)
		ags.append(away_goals)
		num_matches.append(matches)

		data.append((league_name, score, home_goals, away_goals, matches))

df = pd.DataFrame({'League': league,
	'Score': scores, 'Home Goals': hgs,
	'Away Goals': ags, 'Number of Matches': num_matches})

df = df[['League', 'Score', 'Home Goals', 'Away Goals', 'Number of Matches']]
print(df.info())

df.to_csv('scores_pd.csv')

with open('scores.csv', 'w') as csv_file:
	writer = csv.writer(csv_file)
	for a, b, c, d, e in data:
		writer.writerow([a, b, c, d, e])