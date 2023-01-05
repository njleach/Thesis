cd ../
biber Oxford_Thesis.bcf --output-resolve-crossrefs --output_format=bibtex
mv Oxford_Thesis_biber.bib bib-info/
cd bib-info
bib2xml Oxford_Thesis_biber.bib > Oxford_Thesis_biber.xml
xml2ris Oxford_Thesis_biber.xml > Oxford_Thesis_biber.ris
python clean_ris.py
ris2xml Oxford_Thesis_biber_clean.ris > Oxford_Thesis_biber_clean.xml
xml2bib Oxford_Thesis_biber_clean.xml > Oxford_Thesis_biber_clean.bib
