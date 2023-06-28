#!/usr/bin/python
# Written in Python 3.7 in 2023 by A.L.O. Gaenssle
# KRONA DATA EXTRACTOR - MAIN SCRIPT

##------------------------------------------------------
## IMPORT MODULES
##------------------------------------------------------
import sys
import os
import pandas as pd

# Own modules
# import Import_Export as IE
import Extract_Krona as Extract

##------------------------------------------------------
## FUNCTIONS
##------------------------------------------------------
# Print header
def print_header():
	print("\n","-"*75,"\n","-"*75)
	print("\tTHE KRONA DATA EXTRACTOR\tby A.L.O. Gaenssle, 2023")
	print("", "-"*75,"\n")

# Ask if the taxonomy should be counted
def get_taxonomy():
	answer = input("\nDo you want to count the taxonomy?"
		"\n(y=yes, n=no)\n")
	while answer not in ("y", "n"):
		answer = input("\nPlease enter 'y' or 'n'!\n")
	if answer == "y":
		get = True
	else:
		get = False
	return(get)

# Create new Folder
def create_folder(new_path):
	if not os.path.exists(new_path):
		os.makedirs(new_path)
		print("Created folder:", new_path)
	else:
		print("Files will be added to:", new_path)
	return(new_path)

# Get numer & name of all samples
# Return level & name of available taxonomy
def get_samples(header_list, end="Domain"):
	try:
		index = header_list.index(end)
		return(header_list[:index], header_list[index:], index)
	except:
		print("Error: Tag", end, "does not exist")
		return([], [], 0)

##------------------------------------------------------
## MAIN SCRIPT
##------------------------------------------------------
Cutoff = 2000 # Cufoff all UTFs below this number of reads (default = 20000)

print_header()

try:
	input_file = sys.argv[1]
	folder = os.path.split(input_file)[0]
except IndexError:
	folder = "Test/"
	input_file = folder + "Test_krona_plot.html"
	# input_file = folder + "Test_krona_plot_Reads.txt"
file_type = input_file.rsplit(".",1)[1]
get = True # Default for count taxonomy


## Input and extract krona.html file, export into table
if file_type == "html":
	with open(input_file, 'r') as file:
		print("Import File:", input_file)
		input_data = file.read().splitlines()
	sample_list = Extract.GetSamples(input_data)
	Extract.GetReads(input_data, input_file, sample_list)
	get = get_taxonomy()

## Count Taxonomy
if file_type == "txt" or get:
	output_folder = create_folder(folder +"/Results/")
	if file_type != "txt":
		input_file = input_file.rsplit(".",1)[0] + "_Reads.txt"
	reads_df = pd.read_csv(input_file, sep="\t", index_col=False)
	sample_list, level_list, index = get_samples(list(reads_df))
	reads_df[sample_list] = reads_df[sample_list].astype("Int64")
	for level in range(len(level_list)):
		reads = reads_df.groupby(level_list[:level+1], as_index=False)[sample_list].sum()
		species = reads_df.groupby(level_list[:level+1])[sample_list].count()
		if level > 0:
			df = reads[(reads[sample_list] < Cutoff).all(axis=1)]
			df = df.groupby(level_list[:level], as_index=False)[sample_list].sum()
			df.insert(loc=level-1, column=level_list[level], value=["Other"]*len(df))
			reads_filtered = pd.concat([reads[(reads[sample_list] >= Cutoff).any(axis=1)], df])
			reads_filtered.to_csv(file_name + "_Reads_Cutoff" + str(Cutoff) + ".txt", sep="\t", index=False)
		file_name = output_folder + os.path.split(input_file)[0].rsplit(".",1)[0] + "_" + level_list[level]
		reads.to_csv(file_name + "_Reads.txt", sep="\t", index=False)
		species.to_csv(file_name + "_Species.txt", sep="\t")
		print("Counted", level_list[level], "from", input_file)


print("\n","-"*75,"\n End of program\n","-"*75,"\n","-"*75)
