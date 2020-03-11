#This program selects a stratified random sample of annual reports for the purposes of hand-coding
#Date: October 10, 2019
#Author: Carly Knight

import os
import random
import shutil
import re


origin_files = "/Users/carlyknight/Documents/Data/Annual Report/report_paragraphs/future_texts/"
pdf_loc = "/Users/carlyknight/Documents/Data/Annual Report/PDF/"
destination= "/Users/carlyknight/Dropbox/PROJECTS/ConceptionsofRisk/Corporate_Futures_for_Hesu/files_for_RA"


#randomly select set of 10 files from customer
n=10
future_files= os.listdir(origin_files)
set1=random.sample(future_files,n)
for file in set1:
	shutil.copy(os.path.join(origin_files, file), destination)

#get list of all pdfs
filelist = []
for dirName, subdirList, fileList in os.walk(pdf_loc, topdown=False):
    for fname in fileList:
    	if fname.endswith('.pdf'):
    		filelist.append(os.path.join(dirName, fname))

#get number of matches
textfiles=[]
for file in set1:
	textfiles.append(file.replace(".txt", ""))

#iterate though list of pdfs and find matches:
matches=[]
for file in filelist:
	try:
		num = re.search(r'([0-9]{6,12}(?=\.pdf))', file).group(0)
	except Exception:
		pass
	if num in textfiles:
		matches.append(file)

#move pdfs to samples
for file in matches:
	shutil.copy(file, destination)









