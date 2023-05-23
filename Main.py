#!/usr/bin/python
# Written in Python 3.7 in 2023 by A.L.O. Gaenssle
# KRONA DATA EXTRACTOR - MAIN SCRIPT

##------------------------------------------------------
## IMPORT MODULES
##------------------------------------------------------
import sys
import os

# Own modules
import Import_Export as IE
import Extract_Krona as Extract
import Combine_Files as Combine
import Count_Taxonomy as Count

##------------------------------------------------------
## FUNCTIONS
##------------------------------------------------------
# Print header
def PrintHeader():
    print("\n","-"*75,"\n","-"*75)
    print("\tTHE KRONA DATA EXTRACTOR\tby A.L.O. Gaenssle, 2023")
    print("", "-"*75,"\n")

def GetTaxonomy():
	Answer = input("\nDo you want to count the taxonomy?"
		"\n(y=yes, n=no)\n")
	while Answer not in ("y", "n"):
		Answer = input("\nPlease enter 'y' or 'n'!\n")
	if Answer == "y":
		Get = True
	else:
		Get = False
	return(Get)

##------------------------------------------------------
## MAIN SCRIPT
##------------------------------------------------------
Cutoff = 20000 # Cufoff all UTFs below this number of reads (default = 20000)

PrintHeader()

try:
	InputFile = sys.argv[1]
	Folder = os.path.split(InputFile)[0]
except IndexError:
	Folder = "Test/"
	InputFile = Folder + "Test.krona_plot.html"
FileType = InputFile.rsplit(".",1)[1]
Get = True # Default for count taxonomy


## Input and extract krona.html file, export into table
if FileType == "html":
	InputData = IE.ImportList(InputFile, Strip=False)
	SampleList = Extract.GetSamples(InputData)
	ReadList, Header = Extract.GetReads(InputData, InputFile, SampleList)
	Get = GetTaxonomy()

## Count Taxonomy
if FileType == "txt" or Get:
	OutputFolder = IE.CreateFolder(Folder+"/Results/")
	if FileType == "txt":
		ReadList, Header = IE.ImportNestedList(InputFile, getHeader=True)
	SampleList, LevelList, Index = Count.GetSamples(Header)
	for Level in range(len(LevelList)):
		OutputFile = OutputFolder + os.path.split(InputFile)[0].rsplit(".",1)[0] + "_" + LevelList[Level] + ".txt"
		Header = "\t" + "\t".join(SampleList) + "\n"
		LevelReads = Count.CountLevel(ReadList, Index, Level, OutputFile, Header)
		if Level > 0:
			filteredReads = Count.FilterReads(LevelReads, Cutoff, OutputFile, Header)


## Combine Files
# InputFile1 = Folder + "Name1" + ".krona_plot_Reads.txt"
# InputFile2 = Folder + "Name2" + ".krona_plot_Reads.txt"
# OutputFile =Folder + "Name" + ".krona_plot_Reads.txt"
# CombineFiles(InputFile1, InputFile2, OutputFile)

print("\n","-"*75,"\n End of program\n","-"*75,"\n","-"*75)
