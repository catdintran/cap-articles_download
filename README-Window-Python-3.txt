# platform : win-64
# conda version : 4.3.8

# pdfMiner is not compartible with Python 3.*
# in order to include pdfMiner to your IDE, follow this steps in anaconda

conda install -c conda-forge pdfminer.six

-> choose 'y' to proceed

# open your IDE, run file pdf_to_html_pdfminer6.py
# path1 = directory where you store .pdf files
# path2 = directory where the converted html files located