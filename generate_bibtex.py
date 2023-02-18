# -*- coding: utf-8 -*-
"""generate_bibtex.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QcOoyU6a-FEiWdNpZNm5YzEV9vDDfK5m

# Script for generating bibtex of a research article 
Authors: Kanchan Soni, ChatGPT

* Before using this script, ensure that you have the pybtex and requests libraries installed in your local environment.

* To use this script, provide the DOI of the research article for which you want to generate a BibTeX entry. Run the script, and it will generate a BibTeX entry in the format accepted by Physical Review D.
"""

!pip install pybtex==0.22.2
!pip install requests==2.28.0

from pybtex.database import BibliographyData, Entry
from pybtex.database.input import bibtex
import requests


def gen_bibtex(input_doi):
  # construct the CrossRef API URL to retrieve metadata for the article
  crossref_api_url = f'https://api.crossref.org/works/{input_doi}'

  # send a GET request to the CrossRef API
  response = requests.get(crossref_api_url)


  # extract the BibTeX from the CrossRef metadata
  if response.status_code == 200:
      data = response.json()['message']
      fields = {
          'title': data['title'][0],
          'author': ' and '.join([f"{a['given']} {a['family']}" for a in data['author']]),
          'journal': data['container-title'][0],
          'volume': data['volume'],
          'number': data['issue'],
          'year': str(data.get('published-print', {}).get('date-parts', [[None]*3])[0][0] or data.get('published-online', {}).get('date-parts', [[None]*3])[0][0] or ''),
          'month': str(data.get('published-print', {}).get('date-parts', [[None]*3])[0][1] or data.get('published-online', {}).get('date-parts', [[None]*3])[0][1] or ''),
          'publisher': data['publisher'],
          'doi': doi,
          'url': data['URL']
      }
      if 'page' in data:
          fields['pages'] = data['page']
      entry = Entry('article', fields=fields)
      bib_data = BibliographyData(entries={doi: entry})
      bibtex = bib_data.to_string('bibtex')
      print(bibtex.encode('utf-8').decode('utf-8'))
  else:
      print(f"Error: HTTP status code {response.status_code}")

# enter the DOI of the research article

doi = "10.1103/PhysRevD.95.042001"

# Generate the bibtex in the PRD format 
gen_bibtex(doi)

