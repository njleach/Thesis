"""
This is a little script that simply orders 
the items in abbreviations.tex

Items betweem `\begin` and  `\end` are ordered.
"""

keys = []
values = []

## read in to generate key/value dict of abbreviations
with open("./abbreviations.tex","r") as f:
	for line in f:
		if line.lstrip()[:5] == '\item':

			s1 = line.partition('[')[-1].partition(']')
			keys += [s1[0]]
			values += [s1[-1][1:]]

dict = dict(zip(keys[:],values[:]))
keysort = sorted(keys)
text = ""
itemformat = "    \item[{}] {}"

## read in again to generate full text
with open("./abbreviations.tex","r") as f:
	for line in f:
		if line.lstrip()[:5] == '\item':
			key = keysort.pop(0)
			text += itemformat.format(key,dict[key])
		else:
			text+=line

## write text to file
with open('./abbreviations.tex','w') as f:
	f.write(text)
