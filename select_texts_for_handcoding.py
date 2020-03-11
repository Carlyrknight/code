#This program selects a stratified random sample of annual reports for the purposes of hand-coding
#Date: October 10, 2019
#Author: Carly Knight

import os
import random
import shutil
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

xml_files = "/Users/carlyknight/Documents/Data/Annual Report/XML/"
destination= "/Users/carlyknight/Dropbox/PROJECTS/Corporate_Futures_for_Hesu/files_for_RA/"


#identify zipfiles
zippaths=[]
for zipped in os.listdir(xml_files):
	if not zipped.endswith('.zip'):continue
	zippaths.append(os.path.join(xml_files, zipped))

#identify files that I want 
selected=[]
for file in os.listdir(destination):
	if file.endswith('.txt'):
		selected.append(file.replace('.txt', '.xml'))

#function to get text
def get_fulltext(root):
	full = root.find('FullText')
	if full is None:
		fulltext = ""
	else:
		fulltext=full.text
	return fulltext


#iterate through zippaths
for filename in zippaths:
	with ZipFile(filename, "r") as zf:
		for name in zf.namelist():
			if name in selected:
				print("Found one!")
				data= zf.read(name)
				root = ET.fromstring(data)
				fulltext= get_fulltext(root)
				with open(destination + re.sub(".xml", ".txt", "fulltext_" + name), "w") as text_file:
					_=text_file.write(fulltext)



n=10
future_files= os.listdir(origin_files)
set1=random.sample(future_files,n)
for file in set1:
	shutil.copy(os.path.join(origin_files, file), destination)

#get list of all pdfs
exclude = set(map(str, range(1844, 1930)))

filelist = []
for dirName, subdirList, fileList in os.walk(pdf_loc, topdown=True):
	subdirList[:] = [d for d in subdirList if d not in exclude]
	for fname in fileList:
		if fname.endswith('.pdf'):
			filelist.append(os.path.join(dirName, fname))

#37,960

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









