cd ../
biber Oxford_Thesis.bcf --output-resolve-crossrefs --output_format=bibtex
mv Oxford_Thesis_biber.bib bib-info/
cd bib-info
bib2xml Oxford_Thesis_biber.bib > Oxford_Thesis_biber.xml
xml2ris Oxford_Thesis_biber.xml > Oxford_Thesis_biber.ris
python clean_ris.py
