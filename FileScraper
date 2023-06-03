from cgitb import html
import requests
import pdfminer
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import os


## Computing URLs of pdf files on PubMed Database (https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_pdf/)
def findlinks(L, mode='id'):
    response = requests.get(L)
    page = BeautifulSoup(response.text, "html.parser")
    links = page.find_all('a')
    Output = []
    for l in links:
        href = l['href']
        if mode=='id' and len(href) == 3:
            Output.append(L + str(href))
        elif mode=='pdf':
            hrefstr = str(href)
            if hrefstr[-4:] == '.pdf':
                Output.append(L + str(href))
    return(Output)

## Extraction
url = "https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_pdf/"
pdfs = [z for x in findlinks(url,'id')[0:2] for y in findlinks(x,'id')[0:5] for z in findlinks(y,'pdf')]

## Change output_dir to a suitable directory for your computer
output_dir = '/Users/josiahwu29/Desktop/ResearchPapers'
filepaths = []

## Storage
for i in range(0,200):
    l = pdfs[i]
    response = requests.get(l)
    if response.status_code == 200:
        file_path = os.path.join(output_dir, os.path.basename(l))
        filepaths.append(file_path)
        with open(file_path, 'wb') as f: ##
            f.write(response.content)
    print(i)


