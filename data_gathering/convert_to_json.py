# This script just converts a csv file to a JSON file

# Here is an example of how it is used to convert filename.csv to a JSON file outputname.json
# 	python convert_to_json filename.csv outputname.json

import sys
import pandas as pd

# Check that the correct number of arguments are passed
assert len(sys.argv) == 2 or len(sys.argv) == 3, "Error, %d arguments passed to %s, but 2 or 3 are required (filename, outputname (optional))!" %(len(sys.argv)-1,sys.argv[0])

df = pd.read_csv(sys.argv[1])

if len(sys.argv) == 3:
	df.to_json(outputname, orient='records')
else:
	df.to_json(sys.argv[1][:-3] + "json", orient="records")