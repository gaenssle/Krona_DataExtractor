# DataExtractor for Krona.html files
created 2023 by gaenssle
written in python 3.8

for questions, write to algaenssle@gmx.com

Krona plots (https://github.com/marbl/Krona/wiki) create interactive html files for hierachical metagenomic visualization.

This program here
- extracts the data stored in krona.html files (e.g. for creating tables)
- sums the reads and counts the occurence of species in each Domain, Phylum, Class, Order, Family, Genus and Species
- it creates files with and without a cutoff (e.g. 20,000 reads)

Run the script:
- The program is started over the terminal by typing:
python3 Main.py [File]
where [File] is the input file you want to use

Accepted input files:
- krona.html (to extract them to a spreadsheet .txt file)
- krona_Reads.txt (extracted files, to count taxonomy)
The program will automatically determine which file type it is and for .html files it will ask if you want to conduct the counting of the taxonomy as well
