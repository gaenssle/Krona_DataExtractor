#!/usr/bin/python
# Written in Python 3.7 in 2023 by A.L.O. Gaenssle
# Module of Krona Data Extractor
# -> Extracts data from krona.html files as saves them as tables

import copy
import pandas as pd

##------------------------------------------------------
## FUNCTIONS
##------------------------------------------------------

# Get sample number and names
def GetSamples(InputData):
	SampleList = []
	for Line in InputData:
		if Line.strip().startswith("<dataset>"):
			Sample = Line.split(">",1)[1]
			SampleList.append(Sample.split("<",1)[0])
			if Line.strip().startswith("</datasets>"):
				break
	return(SampleList)


# Extract all reads for each sample and Species
# -> save as [Sample1, Sample2,... Domain, Phylum, Class...]
def GetReads(InputData, InputFile, SampleList):
	ReadList = []
	Tree = [""] * 10
	Level = 0
	for Index in range(0,len(InputData)):
		if InputData[Index].strip().startswith("<node"):
			Indent, Line = InputData[Index].split("<",1)
			Name = Line.split("name=",1)[1].replace(">","").replace("\"","").replace("_"," ").strip()
			for i in range(len(Indent), Level+1):
				Tree[i] = ""
			Level = len(Indent)
			Tree[Level] = Name
			if " " in Name and not "unclassified" in Name:
				if InputData[Index+1].strip().startswith("<magnitude"):
					Reads = []
					ReadsLine = InputData[Index+1].split("<val>")[1:]
					for Sample in ReadsLine:
						Reads.append(Sample.split("<",1)[0])
					for Fill in range(len(Reads),len(SampleList)):
						Reads.append("")
					Reads.extend(copy.deepcopy(Tree[1:]))
					ReadList.append(Reads)
	OutputFile = InputFile.rsplit(".",1)[0] + "_Reads.txt"
	Header = SampleList + ["Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Subspecies", ""]
	df = pd.DataFrame(ReadList,columns=Header)
	df.drop("", axis=1, inplace=True)
	df.to_csv(OutputFile, sep="\t", index=False)
