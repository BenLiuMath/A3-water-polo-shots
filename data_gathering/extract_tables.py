# This script extracts tables from pdf files using tabula-py.
# It then cleans up the data, before saving as a csv file.
# We do not remove any data at this point (other than overall scores)

# To download tabula-py with pip, run
# 	pip install tablua-py

# To download the Women's play-by-play pdfs, navigate to the directory where you want
# the files placed and run the following commands in the command line:
# 	for ((i=1; i<=9; i++)) do wget  http://waterpolo.sportresult.com/pdf/WCH2017/W0${i}hr.pdf; done
# 	for ((i=10; i<=48; i++)) do wget  http://waterpolo.sportresult.com/pdf/WCH2017/W${i}hr.pdf; done


# ----------------------------------------------------------------------------
# 								Parameters
# ----------------------------------------------------------------------------

# num_games             = 48			# Total number of games in the data set
# base_prefix           = "data/raw/W"		# 
# base_postfix          = "hr.pdf"
# game_list_filename = "data/team-game_pairings.csv"

# ----------------------------------------------------------------------------


import pandas as pd
from tabula import read_pdf
import sys

# 
# Read in file names and parameters from the command line
# 

# Check that the correct number of arguments are passed
assert len(sys.argv) == 6, "Error, %d arguments passed to %s, but 5 are required!" %(len(sys.argv)-1,sys.argv[0])

# Read in the arguments
base_prefix        = sys.argv[1]			# Start of pdf file names
base_postfix       = sys.argv[2] + ".pdf"	# End of pdf file names
num_games          = int(sys.argv[3])		# Total games in the data set
game_list_filename = sys.argv[4]			# Where to output game list
sex 			   = sys.argv[5]

base_prefix 	   = base_prefix + "/" + sex

# Reads in and cleans up a single pdf file
def clean_file(f_name):
	print "Working on file: %s..." %(f_name)

	# Read in the pdf file as a pandas dataframe object

	df_left  = read_pdf_improved(f_name);

	# Combine two side-by-side tables into one
	df_right = fix_names(df_left.loc[:,df_left.columns[6:]])
	df_left  = fix_names(df_left.loc[:,df_left.columns[0:6]])
	df       = pd.concat([df_left, df_right], axis=0, ignore_index=True)

	# Determine home and away teams
	home_away_list = infer_home_and_away(df)

	# Fill in empty score entries
	df['Score'] = df['Score'].fillna(method='pad').fillna(value="0 - 0")

	# Create columns for home and away teams
	df[home_away_list[0]] , df[home_away_list[1]] = df['Score'].str.split(' - ',1).str

	# Fill out the missing period entries
	df.Period = df.Period.fillna(method='pad')

	# Add in column measuring seconds left in the quarter
	df.dropna(axis=0, subset=['Time'], inplace=True)	# Remove rows with no time entries
	def time_to_seconds(s):
		return int(s.split(':')[0]) * 60 + int(s.split(':')[1])
	df['Seconds'] = df.Time.map(lambda s: time_to_seconds(str(s)))

	# Output as a CSV file with the same name
	df.to_csv(f_name[:-4] + ".csv", index=False)

	# Return the two teams
	return home_away_list


# Fix the column names (they get broken up strangely by the converter)
def fix_names(df):
	if "Score Team Cap" in df.columns or "Score Team Cap.1" in df.columns:
		# Check if looking at right-hand df and if so, prime names for next step
		if "Period.1" in df.columns:
			df = df.rename(
				index=str,
				columns={"Period.1" : "Period", "Time.1" : "Time", "Action.1" : "Action", "Score Team Cap.1" : "Score Team Cap", "Unnamed: 10" : "Unnamed: 4", "Player.1" : "Player"})

		# Rename incorrect columns
		df = df.rename(
			index=str,
			columns={"Score Team Cap" : "Team", "Unnamed: 4" : "Cap"})

		# Extract score entry and give its own column
		df['Score'] = None
		df['Team']  = df['Team'].astype(str)
		score_idx   = df.Team.apply(len) > 3
		df.loc[score_idx,'Score'] = df.loc[score_idx,'Team'].map(lambda s: s[:-4])	# Get the score from the other column

		# Remove the score from the name column (the table extractor combines the two)
		df.Team = df.Team.map(lambda s: s if len(s) == 3 else s[-3:])

		return df

	elif "Team Cap" in df.columns or "Team Cap.1" in df.columns:
		# Check if right-hand df and if so, prime names for next step
		if "Period.1" in df.columns:
			df = df.rename(
				index=str,
				columns={"Period.1" : "Period","Time.1" : "Time", "Action.1" : "Action", "Score.1" : "Score", "Team Cap.1" : "Team Cap", "Player.1" : "Player"})

		# Fix some of the column names
		df = df.rename(index=str, columns={"Team Cap" : "Team"})
		df['Team'] = df['Team'].astype(str)

		# Extract Cap entry and give its own column
		df['Cap'] = df['Team'].map(lambda s: s[4:] if len(s) > 4 else None)

		# Adjust Team column so it no longer includes cap information
		df['Team'] = df['Team'].map(lambda s: s[:3])

		return df

	else:
		print df.columns
		assert 1==0, "Error. Previous cases didn't cover this one."

# Function for reading in the pdf file and converting it into a DataFrame.
# Checks whether table bleeds onto second page of pdf
def read_pdf_improved(f_name):
	# Check whether the table bleeds onto second page
	all_tables = read_pdf(f_name,pages="1-2",multiple_tables=True)
	top_table  = read_pdf(f_name)

	# pdb.set_trace()

	if (all_tables[1].shape[1] == 12):		# The table does bleed over
		all_tables[1].columns = top_table.columns
		return pd.concat([top_table, all_tables[1].loc[1:]], axis=0, ignore_index=True)

		# # Make sure the columns in the pg. 2 tables align with those in the pg. 1 tables
		# top_cols = top_table.columns.values
		# bot_cols = all_tables[1].columns.values
		# def f(x):
		# 	return str(x[bot_cols[3]]) + " " + str(x[bot_cols[4]])
		# if pd.isnull(top_table[top_cols[3]][1]):
		# 	if pd.isnull(all_tables[1][bot_cols[3]][1]):
		# 		pass		# It already matches
		# 	else: 			# We need to combine everything into column 4
		# 		all_tables[1][bot_cols[3]] = all_tables[1].apply(lambda x: str(x[bot_cols[3]]) + " " + str(x[bot_cols[4]]))

		# # Else the column contains country data
		# elif len(str(top_table[top_cols[3]][1])) == 3:




	else:
		return top_table

# Determine which team is the home team and which is the away team
# 	Returns a list of the two team names in an order corresponding
# 	to the entries in the score column.
def infer_home_and_away(df):
	# Find index of first time a team scores
	score_idx = df['Score'].first_valid_index()

	# Figure out which team scored
	scoring_team = df.loc[score_idx,'Team']

	# Figure out the other team
	for team in df['Team']:
		if team != scoring_team:
			other_team = team
			break

	# Figure out which score entry changed
	scores = df.loc[score_idx,'Score'].split(' - ')

	# Place team names in appropriate order in output list
	if scores[0] == "1":
		return [scoring_team, other_team]
	else:
		return [other_team, scoring_team]



# Loop over all the game pdfs, extract and clean up the tables, write as csv files.
# Track which teams are associated with which file

game_list_file = open(game_list_filename, 'w')
game_list_file.write("Team 1,Team 2\n")

# teams = clean_file(base_prefix + "32" + base_postfix)


# pdb.set_trace()

# First 9 have a 0
for n in xrange(1,10):
	teams = clean_file(base_prefix + "0" + str(n) + base_postfix)
	game_list_file.write("%s,%s\n" %(str(teams[0]),str(teams[1])))

for n in xrange(10,num_games+1):
	teams = clean_file(base_prefix + str(n) + base_postfix)
	game_list_file.write("%s,%s\n" %(str(teams[0]),str(teams[1])))
