# This script splits the action column into three new columns:
# the action is retained, the result is put in a new column,
# and a binary column indicating whether a goal was scored is
# added in a third column.
# This way we can more easily track whether shots were successful

import pandas as pd

# Name of the file to work on (actions must consist only of shots)
team_of_interest = "BRA"
filename         = "data/processed/" + team_of_interest + "/W_" + team_of_interest + "_shots"

# Read in the file
df = pd.read_csv(filename + ".csv")

# Split the action column
new_cols = df['Action'].apply(lambda r: pd.Series(r.split(' - ')))

df['Action'] = new_cols.loc[:,0]
df['Result'] = new_cols.loc[:,1]

# Result consists of multiple possibilities: Goal, Missed, Saved, Blocked, Post
df['Goal'] = df['Result'].map(lambda r: 1 if r == "Goal" else 0)

# Save the result
df.to_csv(filename + "_processed.csv", index=False)
df.to_json(filename + "_processed.json", orient='records')
