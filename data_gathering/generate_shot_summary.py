# This script generates csv and json files summarizing each player's shots
# in each game

import pandas as pd
import sys

# ----------------------------------------------------------------------------
# 								Parameters
# ----------------------------------------------------------------------------

assert len(sys.argv) == 4, "Error, %d arguments passed to %s, but 3 are required!" %(len(sys.argv)-1,sys.argv[0])

team_of_interest = sys.argv[1]
input_filename   = sys.argv[2]
output_filename  = sys.argv[3]

# team_of_interest = "BRA"
# input_filename  = "data/processed/" + team_of_interest + "/W_" + team_of_interest + "_shots_processed"
# output_filename = "data/processed/" + team_of_interest + "/W_" + team_of_interest + "_shots_summary"

# ----------------------------------------------------------------------------


# Read in the data
df_in = pd.read_csv(input_filename)

# Filter out data from other teams
df_in = df_in[df_in['Team'] == team_of_interest]

# Create a new DataFrame in which to store the new table
cols = ['Player','Game','Action','Goal']
df   = pd.pivot_table(df_in[cols], index=['Player','Game'], columns='Action', aggfunc=[len,sum], fill_value=0)

# Compute total shots taken by each player in each game and total made in each game
total_attempts = df['len']['Goal'].sum(axis=1)
total_made     = df['sum']['Goal'].sum(axis=1)

# Fix the hierarchical indexing to be human readable
df.columns.set_levels([' attempted' ,' made'], level=0, inplace=True)
new_col_inds = pd.Index([e[2] + e[0] for e in df.columns.tolist()])
df.columns   = new_col_inds

# Add in the total columns
df['Total attempted'] = total_attempts
df['Total made']      = total_made

# Output the data to a csv file
df.to_csv(output_filename)

# Read in csv file we just created to fill in the hierarchical indices
df = pd.read_csv(output_filename)

# Write to a JSON file
df.to_json(output_filename[:-3] + "json", orient="records")