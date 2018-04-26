# This script combines all the csv files in a set into one large
# csv file with additional fields: Game, Opponent, and Opponent name

import pandas as pd

# ---------------------------------------------------------------------
# 						Parameters
# ---------------------------------------------------------------------
# Which games to concatenate
team_of_interest      = "USA"	      					# Team we're interested in
output_filename       = "data/processed/" + team_of_interest + "/W_" + team_of_interest
shots_only_filename   = "data/processed/" + team_of_interest + "/W_" + team_of_interest + "_shots"
base_prefix           = "data/raw/W"
base_postfix          = "hr.csv"
team_game_table_fname = "data/team-file_pairings.csv"

# ---------------------------------------------------------------------


# Figure out which games the team of interest played in
all_games = pd.read_csv(team_game_table_fname)
game_list = all_games[(all_games['Team 1'] == team_of_interest) | (all_games['Team 2'] == team_of_interest)].index.values + 1

# # Games that various womens teams played in
# # (Use this command: awk '/$TEAMCODE/ {print FNR}' data/game_list.txt )
# # TODO: automate this by having this script read through data/game_list.txt
# # Most of these probably have at least one wrong entry...

# game_dict = {"USA": ["04", "09", "23", "36", "43", "48"],
# 			"BRA" : ["02", "16", "22", "25", "32"],
# 			"ESP" : ["03", "09", "24", "28", "38", "44", "48"],
# 			"RUS" : ["08", "13", "19", "29", "35", "43", "47"],
# 			"CAN" : ["01", "14", "21", "27", "37", "44", "47"],
# 			"ITA" : ["01", "16", "20", "35", "41", "46"],
# 			"HUN" : ["07", "15", "23", "37", "42", "46"],
# 			"AUS" : ["06", "13", "18", "30", "36", "41", "45"],
# 			"GRE" : ["08", "12", "18", "38", "42", "45"],
# 			}


# Write a list of the teams to a text file
team_list      = set(all_games['Team 1'].values).union(set(all_games['Team 2'].values))
team_list_file = open('team_list.txt', 'w')
for item in team_list:
	team_list_file.write("%s\n" %(item))


# Read in data for all the games the team of interest played and append
# to one large DataFrame, then save it
df_global = pd.DataFrame()

game = 1
for game_number in game_list:
	# Read in csv and append it to the global DataFrame
	if (game_number < 10):
		df = pd.read_csv(base_prefix + "0" + str(game_number) + base_postfix)
	else:
		df = pd.read_csv(base_prefix + str(game_number) + base_postfix)

	df["Game"] = game

	# Change column of other team to 'Opponent'
	for team in df["Team"]:
		if team != team_of_interest:
			opponent = team
			break
	df = df.rename(index=str, columns={opponent : "Opponent"})

	# Add Opponent name column
	df["Opponent name"] = opponent

	df_global = df_global.append(df,ignore_index=True)
	game += 1

# Save the results
df_global.to_csv(output_filename + ".csv", index=False)
df_global.to_json(output_filename + ".JSON", orient="records")


# Create a csv file with just the column names
df_temp = pd.DataFrame(columns=df_global.columns)
df_temp.to_csv(shots_only_filename + ".csv", index=False)

# To isolate the lines that contain a shot, run the following
# command in the command line:
#	grep "^.*\([Sh]ot\|[Cc]ounter attack\)" ***output_filename*** >> ***shots_only_filename***
