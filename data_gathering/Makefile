# Makefile for generating the data files for A3 (water polo shots)


# Files containing variables and paths
# The main one you will probably want to edit is the TEAM variable in paths.mk
include variables.mk
include paths.mk



## team_data 			: Generates all data files that need to be updated for the specified team
.PHONY : team_data
team_data : $(SHOT_SUMMARY_FILE) $(ALL_ACTIONS_FILE)



# Generate a JSON file from a csv file
# If you want to generate filename.json from an existing csv file filename.csv, run
# 	make filename.json
%.json : %.csv $(CONVERT_TO_JSON_SRC)
	python $(CONVERT_TO_JSON_SRC) $< $@


# Extract data from the pdfs directly (after specifying a year and sex)
# $(CSV_FILES) $(GAME_LIST_FILE) : $(EXTRACT_TABLES_SRC) $(PDF_FILES) variables.mk
$(GAME_LIST_FILE) : $(EXTRACT_TABLES_SRC) $(PDF_FILES) variables.mk
	python $(EXTRACT_TABLES_SRC) $(RAW_PATH) $(PDF_TYPE) $(NUM_GAMES) $(GAME_LIST_FILE) $(SEX)


# Generate file summarizing all actions and another of just the shots for a given team
# $(SHOTS_FILE) $(ALL_ACTIONS_FILE) : $(GROUP_BY_TEAM_SRC) $(CSV_FILES) $(GAME_LIST_FILE) $(SPLIT_ACTION_COL_SRC) paths.mk
$(SHOTS_FILE) $(ALL_ACTIONS_FILE) $(TEAM_LIST_FILE) : $(GROUP_BY_TEAM_SRC) $(GAME_LIST_FILE) $(SPLIT_ACTION_COL_SRC) paths.mk
	python $(GROUP_BY_TEAM_SRC) $(TEAM) $(ALL_ACTIONS_FILE) $(SHOTS_FILE) $(RAW_PATH) $(PDF_TYPE) $(GAME_LIST_FILE) $(SEX) $(TEAM_PATH) $(TEAM_LIST_FILE)
	grep "^.*\([Sh]ot\|[Cc]ounter attack\)" $(ALL_ACTIONS_FILE) >> $(SHOTS_FILE)
	python $(SPLIT_ACTION_COL_SRC) $(SHOTS_FILE) 


# Generate shot summary file
$(SHOT_SUMMARY_FILE) : $(SHOT_SUMMARY_SRC) $(SHOTS_FILE)
	python $(SHOT_SUMMARY_SRC) $(TEAM) $(SHOTS_FILE) $(SHOT_SUMMARY_FILE)




# TODO
## parameters							: Print some of the current parameters
.PHONY : parameters
parameters : 
	@echo TEAM: $(TEAM)
	@echo SEX: $(SEX)
	@echo YEAR: $(YEAR)
	@echo NUM_GAMES: $(NUM_GAMES)
	@echo PDF_TYPE: $(PDF_TYPE)
	@echo DATA_PATH: $(DATA_PATH)
	@echo RAW_PATH: $(RAW_PATH)
	@echo PROCESSED_PATH: $(PROCESSED_PATH)
	@echo GAME_LIST_FILE: $(GAME_LIST_FILE)
	@echo TEAM_LIST_FILE: $(TEAM_LIST_FILE)
	@echo CSV_FILES: $(CSV_FILES)


# ## help 								: Prints descriptions of all recipes
# .PHONY : help
# help : Makefile
# 	@sed -n 's/^##//p' $<