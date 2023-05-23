#!/usr/bin/python
# Written in Python 3.7 in 2023 by A.L.O. Gaenssle
# Module of Krona_DataExtractor
# -> counts the ocurrence of species by kingdom/phylum/class, etc

import copy
import Import_Export as IE 	# Own module

##------------------------------------------------------
## FUNCTIONS
##------------------------------------------------------

# Get numer & name of all samples
# & return level & name of available taxonomy
def GetSamples(Header, End="Domain"):
	try:
		HeaderList = Header.strip().split("\t")
		Index = HeaderList.index(End)
		return(HeaderList[:Index], HeaderList[Index:], Index)
	except:
		print("Error: Tag", End, "does not exist")
		return([], [], 0)

# Count reads and number of species at the set level
def CountLevel(Data, Index, Level, OutputFile, Header):
	Reads = {}
	Species = {}
	Shift = Index + Level
	for Line in Data:
		Shift = Index + Level
		if Shift >= len(Line):		# correct shift for shorter taxonomic branches
			Shift = -1
		Name = Line[Shift]
		if Level > 0:
			Tag = ""				# make a tag that indicates the taxonomy
			for i in range(Level):
				if Index+i < len(Line):
					try:
						Tag += Line[Index+i][:3]
					except IndexError:
						pass
			Name = Tag + "_" + Name
		if Name not in Reads:
			Reads[Name] = [0] * Index
			Species[Name] = [0] * Index
		for ID in range(Index):
			try:
				Reads[Name][ID] += int(Line[ID])
				Species[Name][ID] += 1
			except ValueError:
				pass
	IE.ExportNestedDictionary(copy.deepcopy(Reads), OutputFile, "Reads" + Header, Add="_Reads", Ask=False)
	IE.ExportNestedDictionary(Species, OutputFile, "Species" + Header, Add="_Species", Ask=False)
	return(Reads)

# Filter out all lines where no samples has reads above the cutoff value
# -> combine them in tax_Other (< cutoff) with MaxTag (=maximum level: 3= kingdom+phylum)
def FilterReads(Data, Cutoff, OutputFile, Header, MaxTag=2):
	FilteredList = {}
	for Name in Data:
		if any(num > Cutoff for num in Data[Name]):
			FilteredList[Name] = Data[Name]
		else:
			Tag = Name.split("_",1)[0][:MaxTag] + "_Other (< " + str(Cutoff) + " reads)"
			if Tag not in FilteredList:
				FilteredList[Tag] = [0] * len(Data[Name])
			for ID in range(len(Data[Name])):
				try:
					FilteredList[Tag][ID] += int(Data[Name][ID])
				except ValueError:
					pass
	Addition = "_min" + str(Cutoff) + "_Reads"
	IE.ExportNestedDictionary(FilteredList, OutputFile, "Reads" + Header, Add=Addition, Ask=False)
	return(FilteredList)
