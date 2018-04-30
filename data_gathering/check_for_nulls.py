# This script checks for null values in the player
# shot summaries and team shot timeline files.

# Everything is hard-coded in for now, but could easily be generalized if needed.

import pandas as pd



team_list = ["FRA", "USA", "ESP", "NED", "CHN", "AUS", "GRE", "CAN", "KAZ", "NZL", "JPN", "HUN", "RSA", "ITA", "RUS", "BRA"]

for team in team_list:

	# Check for null values in team shot timeline file
	df = pd.read_csv("data/2017/W/processed/" + team + "/shots.csv")
	if df.isnull().values.any():
		print "Null values found in shot timeline for %s" %(team)

	# Check for null values in shot summary file
	df = pd.read_csv("data/2017/W/processed/" + team + "/shot_summary.csv")
	if df.isnull().values.any():
		print "Null values found in shot summary for %s" %(team)


