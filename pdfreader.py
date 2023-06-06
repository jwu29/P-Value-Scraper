from cgitb import html
import requests
import pdfminer
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import os
import re
import tabula
import pandas as pd
import math
import csv

## Restoring files from the other file.
output_dir = '/Users/josiahwu29/Desktop/ResearchPapers'
filepaths = os.listdir(output_dir)
filepaths.remove('.DS_Store')

pequalskeyword = ['P=', 'P = ', 'p=','p = ']

def commonindicesA(a, b):
  b_set = set(b)
  return [i for i, v in enumerate(a) if v in b_set]

pvalkeyword = ['P Value', 'P value','p-value','p value','P-value','P-Value']

## Find P-value from Table
def FindTableP2(dir):

    result = []

    try: 
        tables = tabula.read_pdf(dir, pages='all', multiple_tables=True)
    except:
        return result
    
    ## Filtering dataframes which are empty or has dimension 0.
    for i in range(len(tables)-1,-1,-1):
        if tables[i].empty or tables[i].shape[0] == 0 or tables[i].shape[1] == 0:
            del tables[i]
    
    ## Computing values of a 'P-value' column, if it exists.
    for T in tables:
        ColNames = T.columns.tolist()
        ComInd = commonindicesA(ColNames, pvalkeyword)
        if len(ComInd) != 0:
            for j in ComInd:
                PValCol = T.loc[:, ColNames[j]].tolist()
                PValCol = [str(y) for y in PValCol if y == y]
                for x in PValCol:
                    if re.match(r"^0*\.[0-9]+$",x): ## finds "0.xxxx"
                        result.append(float(x))
                    if re.match(r"^<0*\.[0-9]+$",x): ## finds "<0.xxxx"
                        result.append(float(x[1:]))
    return(result)

## Find P-value From Text
def FindP(dir):
    text = str(extract_text(dir))
    Matches = []
    KeyMatch = [word for word in pequalskeyword if word in text]
    if len(KeyMatch) != 0:
        for x in KeyMatch:
            for match in re.finditer(x,text):
                Matches.append(match.end())
        return Matches
    else:
        return False

P_vals = []
acceptcharlist = ['0','1','2','3','4','5','6','7','8','9','.']

## Main Loop; adjust range accordingly
for x in range(0,len(filepaths),1):
    pathname = output_dir + '/' + filepaths[x]
    print(x)
    print(pathname)
    Q = FindP(pathname)

    ## Check if a number comes after 'P='
    if Q != False:
        text = str(extract_text(pathname))
        for i in Q:
            w = i
            if text[w] in acceptcharlist:
                while text[w] in acceptcharlist:
                    w += 1
                if text[w-1] == '.':
                    w -= 1
                if float(text[i:w]) < 1:
                    P_vals.append(float(text[i:w]))
    
    ## Appending elements of Table P values
    R = FindTableP2(pathname)
    for j in R:
        P_vals.append(j)
    print(P_vals)

## Uncomment the below line; FindTableP2 should be working.
#print(FindTableP2(r'/Users/josiahwu29/Desktop/ResearchPapers/JDI-10-745.PMC6497586.pdf'))

## Saving P_vals in a .csv file
def write_to_csv(l):
     with open(r'/Users/josiahwu29/Desktop/P_vals.csv', 'w', newline='') as csvfile:
         writer = csv.writer(csvfile)
         writer.writerows(map(lambda x: [x], l))
write_to_csv(P_vals)  
