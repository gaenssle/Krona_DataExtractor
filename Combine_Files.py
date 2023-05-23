#!/usr/bin/python
# Written in Python 3.7 in 2023 by A.L.O. Gaenssle
# Module of Krona_DataExtractor
# -> combines the output of two krona.html files

import copy
import Import_Export as IE 	# Own module

##------------------------------------------------------
## FUNCTIONS
##------------------------------------------------------

# Helper function of CombineFiles (converts list to dictionary)
def ConvertFile(InputFile):
	Data, Header = IE.ImportNestedList(InputFile, getHeader=True)
	SampleList, LevelList, Index = GetSamples(Header)
	Dict = {}
	for Line in Data:
		Name = "-".join(Line[Index:])
		Dict[Name] = Line[:Index]
	return(Dict, SampleList, LevelList)

# Combine files of different krona plots
def CombineFiles(InputFile1, InputFile2, OutputFile):
	Dict1, Samples1, LevelList1 = ConvertFile(InputFile1)
	Dict2, Samples2, LevelList2 = ConvertFile(InputFile2)
	Samples3 = Samples1 + Samples2
	for Name in Dict2:
		if Name in Dict1:		# if Name in both Dict1 and Dict2
			Dict1[Name].extend(Dict2[Name])
		else:					# if Name only in Dict2
			Dict1[Name] = [""]*len(Samples1) + Dict2[Name]
	for Name in Dict1:
		if Name not in Dict2:	# if Name only in Dict1
			Dict1[Name].extend([""]*len(Samples2))
	Output = []
	for Name in Dict1:
		Line = Dict1[Name] + Name.split("-")
		Output.append(Line)
	Header = "\t".join(Samples3) + "\t" + "\t".join(LevelList1) + "\n"
	IE.ExportNestedList(Output, OutputFile, Header, Ask=False)
