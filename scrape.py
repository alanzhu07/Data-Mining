import csv

import urllib.request as urllib2
from bs4 import BeautifulSoup

from datetime import datetime
import calendar

# initialize BeaultifulSoup
page = urllib2.urlopen('https://myschooldining.com/SMS/?cmd=menus')
soup = BeautifulSoup(page, 'html.parser')

data = []

# find dates
dates = soup.find_all('td')
for date in dates:
	date_str = date.get('this_date')
	print(date_str)

	# convert string to datetime object then convert to weekday
	date_in_datetime = datetime.strptime(date_str, '%m/%d/%y')
	day_str = calendar.day_name[date_in_datetime.weekday()]
	print(day_str)

	# find meals
	meals = date.find_all('span', attrs={'class': 'period-value'})
	for meal in meals:
		meal_str = meal.text.strip()
		print(meal_str)

		#find food items
		food_tag = meal.parent.parent
		food_items = food_tag.find_all('span', attrs={'class': 'item-value'})
		for food_item in food_items:
			food_str = food_item.text.strip()
			print(food_str)
			data.append((date_str, day_str, meal_str, food_str))

# write to csv
with open('index.csv', 'w') as csv_file:
	writer = csv.writer(csv_file)
	for date, day, meal, food in data:
		writer.writerow([date, day, meal, food])

