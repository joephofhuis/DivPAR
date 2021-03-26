# DivPAR
Diversity Perspectives in Annual Reports (DivPAR)

In organizational communication, different perspectives can be identified with regard to management of cultural diversity. Examining the prevalence and development of these perspectives across organizations, sectors, and countries, can reveal much about how views on workplace diversity evolve over time. DivPAR is a digital tool which enables scholars to engage in such research on a large scale. It conducts automated content analysis of corporate annual reports, identifying the presence of three cultural diversity perspectives – the Moral, Market, and Innovation perspectives, based on earlier work by Robin Ely and David Thomas (2001).

For a full description of the development and validation of DivPAR, and an overview of future uses, we'd like to refer you to the following article:

Hofhuis, J., Schafraad, P., Trilling, D., Luca, N., & Van Manen, B. (in press). Automated content analysis of cultural diversity perspectives in annual reports (DivPAR): Development, validation, and future research agenda. Cultural Diversity and Ethnic Minority Psychology.

## Structure of the repository

This repository contains the materials used for the article mentioned above. In particular, it contains the following files and directories:

- `src/analysis.py`: The hart of DivPAR: The script we used to count the diversity perspectives. Takes `data/raw-private/**/**/*.txt.gz` as input and produces `data/intermediate/automatedcoding.csv`.
- `src/analysis/searchstrings.json` The file that defines the regular expressions to operationalize the different diversity perspectives. Used by `src/analysis.py`
- `src/analysis/check_against_goldstandard.ipynb` A jupyter notebook to calculate agreement of our method with manual coding.
- `src/data-processing/pdf2txt`: The script we used to create the plain text files in `data/raw-private/**/**/*.txt.gz`.
- `data/raw-private` - Directory with input data. In our case, texts of annual reports as gzipped plain text files.
- `data/intermediate/automatedcoding.csv` output produced by DivPAR.
