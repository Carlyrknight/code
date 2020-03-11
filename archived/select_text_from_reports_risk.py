'''
This program selects paragraphs that have to do with risk in the reports
#Date: July 15, 2019
#Author: Carly Knight
'''


# import packages
import os
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from xml import etree
import csv
import re
import dateutil.parser as parser
from enchant.tokenize import get_tokenizer
import enchant
from nltk import tokenize
import numpy as np

# link to location of Annual Report XML Files
results= "/Users/carlyknight/Documents/Data/Annual Report/report_paragraphs/"
directory = "/Users/carlyknight/Documents/Data/Annual Report/XML/"

# define word search
risk_words= ["risk", "uncertainty", "uncertain"]

exclude_risk_words= ["not_risk_word_list"]


'''INITIATE SPELLCHECKER'''
d2 = enchant.DictWithPWL("en_US")
tknzr = get_tokenizer("en_US")

'''WORDSEARCH FUNCTIONS'''

#1: break document into text paragraphs 
def identify_paragraphs(fulltext):
	#in entire document
	risk_w = len(rregex.findall(fulltext))
	#splits
	splits= re.split('((\.{3,}[-_\s]*\.{2,}[-_\s]*)|(\_{3,})|(\-{3,})|(\s{3,}[0-9]{1,}\s{3,})|(\s{5,}[A-Z\s]+\s{5,}))', fulltext)
	splits=[split for split in splits if split is not None if split.strip() is not '']
	return splits


#2: search
def find_matches(splits):
	#set paragraph containers   
	rmatches=[]
	rkeysall= []
	numcorrect=0
	totalwords=0
	for i,section in enumerate(splits):
		#select only sections of a certain character length
		if len(section.strip())>50:
			#select only paragraphs not entirely popoulated by numbers
			section2, true, total = select_good_paragraph(section)
			numcorrect+=true
			totalwords+=total
			#if it returned text
			if section2:
				#run a keyword search
				nummatches= len(rregex.findall(section2))
				if nummatches>0:
					rm, rkeys =keyword_search(section2, rmatches)
					rmatches.extend(rm)
					rkeysall.extend([x.lower() for x in rkeys])
					#if there's at least one match, then identify kind of match
	return '####'.join(rmatches), rkeysall, numcorrect, totalwords



#3: identify only paragraphs with a given data quality
def select_good_paragraph(section):
	# keep only paragraphs that aren't just numbers 
	nums=sum(c.isdigit() for c in section)
	numperiods = section.count('.') + section.count('-') + section.count('_')
	#keep sections with spell correctness above .75
	percent_wc, true, total= calculate_percent_correct(section)
	percent_digits = (nums*1.0 + numperiods*1.0)/len(section)
	#remove sections with list of all capitalized words (most likely to be names)
	percent_uppers = (1.0*sum(1 for c in section if c.isupper()))/len(section)
	if percent_digits<.15 and percent_uppers <.5 and percent_wc >.75 :
		return section, true, total 
	else:
		return None, true, total


#4: get start and end of paragraph section with keyword search
def keyword_search(section, rmatches ):
	rm=[]
	rkeys= rregex.findall(section)
	rs= len(rkeys)
	sentences = tokenize.sent_tokenize(section)
	nsentences=np.array(sentences)
	#if matches/sentence greater than .6, then take entire paragraph. Otherwise, take sentence before and after match
	if (rs/len(sentences))>0.6:
		rm.extend([section])
		#print(wregex.findall(section))
	elif rs>0:
		rindices=[]
		for i, sentence in enumerate(sentences):
			if rregex.search(sentence) and not nrregex.search(sentence) :
				rindices.extend([item for item in [i-1, i, i+1] if item >= 0 and item<len(sentences)])
				#print(wregex.findall(section))
		#remove duplicates from indices lists
		rind = [i for n, i in enumerate(rindices) if i not in rindices[:n]] 
		#select sentences that match 
		rm=[' '.join(list(nsentences[rind]))]
	return rm, rkeys

def clean_paragraph_sentences(fulltext):
	fulltext.replace(u'No.', u'No')
	fulltext.replace("\\", "") 
	fulltext.replace("-", "") 
	return fulltext

'''HELPER FUNCTIONS'''
#function to calculate the percent
def calculate_percent_correct(text):
	true =0
	total = 0.0
	for word in tknzr(text):
		word1 =word[0]
		total +=1
		if d2.check(word1):
			true +=1
	if total !=0:
		percent = true*1.0/total
	else:
		percent =0
	return percent, true, total

def get_fulltext(root):
	full = root.find('FullText')
	if full is None:
		fulltext = ""
	else:
		fulltext=full.text
	return fulltext

'''ZIP PATHS'''
zippaths=[]
for zipped in os.listdir(directory):
	if not zipped.endswith('.zip'):continue
	zippaths.append(os.path.join(directory, zipped))


'''COMPILE REGEX PATTERNS'''
#labor
patternr = "(?<=\W)(%s)" % "|".join(risk_words)
rregex = re.compile(patternr, re.IGNORECASE)

'''COMPILE NOT REGEX OPTIONS'''
pattern_nr = "(?<=\W)(%s)" % "|".join(exclude_risk_words)
nrregex = re.compile(pattern_nr)


'''OPEN CSV WRITER'''
csvfile = open(results + 'risk_paragraphs_sample.csv', 'w')
fieldnames = ['Location', 'Filename', 'RecordTitle', 'Date', 'Date1', 'Year', 'URL', 'CompanyName', 'NAIC', 'ClassCode',
			  'Classification', 'AnrAssetDispIdxNum', 'rmatch', 'risk_words', 'percentcorrect', 'numwords'] + risk_words
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()


# '''TEST'''
# filename= "/Users/carlyknight/Documents/Data/Annual Report/XML/HAR_20160830003924_00001.zip"
# name = "88225988.xml"
# with ZipFile(filename, "r") as zf:
# 	data= zf.read(name)
# root = ET.fromstring(data)
# fulltext=clean_paragraph_sentences(get_fulltext(root))
# wfile, sfile, cfile, ws, ss, cs, wkeys, skeys, ckeys = identify_paragraphs(fulltext=fulltext)

'''WRITE'''
i=1
for filename in zippaths:
	with ZipFile(filename, "r") as zf:
		for name in zf.namelist():
			data= zf.read(name)
			root = ET.fromstring(data)
			id = root.find('RecordID').text
			date = root.find('AlphaPubDate').text
			datenum = root.find('NumericPubDate').text
			year = parser.parse(date).year
			url = root.find('URLDocView').text
			child = root.find('Terms')
			for alltags in child.findall('.//'):
				if alltags.tag == "CompanyName":
					company = alltags.text
				elif alltags.tag == "CompanyNAIC":
					naics = alltags.text
				elif alltags.tag == "ClassCode":
					code = alltags.text
				elif alltags.tag == "ClassExpansion":
					classic = alltags.text
			# put the flexterms into a dictionary
			dict = {}
			for elem in root.iter('FlexTerm'):
				dict[elem.find('FlexTermName').text] = elem.find('FlexTermValue').text
			# create terms from dictionary
			ancode, ancashd, ancashs, anasd, anass, anrevd, anrevs, anearnd, anearns = [dict.get(k) for k in
																					['AnrClassCode1IdxLit',
																					 'AnrCashDispIdxNum',
																					 'AnrCashSrchIdxNum',
																					 'AnrAssetDispIdxNum',
																					 'AnrAssetSrchIdxNum',
																					 'AnrRevDispIdxNum',
																					 'AnrRevSrchIdxNum',
																					 'AnrEarnDispIdxNum',
																					 'AnrEarnSrchIdxNum']]
			# if variables above are NONE, recode as empty string
			ancode, ancashd, ancashs, anasd, anass, anrevd, anrevs, anearnd, anearns = [k or "" for k in
																					[ancode, ancashd, ancashs, anasd,
																					 anass, anrevd, anrevs, anearnd,
																					 anearns]]
			#create list of alternative company names
			altnames =[]
			for elem in root.iter('FlexTerm'):
				if elem.find('FlexTermName').text == "AnrRelCoNameIdxLit":
					altnames.append(elem.find('FlexTermValue').text)
			relnames='; '.join(altnames)
			# get full text if available
			fulltext=clean_paragraph_sentences(get_fulltext(root))
			#split text into paragraphs
			splits= identify_paragraphs(fulltext)
			#findmatches
			rfile, rkeys, numcorrect, totalwords = find_matches(splits)
			#calculate percentcorrect
			if totalwords!= 0:
				percentcorrect = numcorrect*1.0/totalwords
			else:
				percentcorrect =0
			print(percentcorrect)
			#put matches in a dictionary
			rdict= {k: rkeys.count(k) for k in risk_words}
			#calculate characteristics of the file
			numwords = len(fulltext.split())
			#save textfile as long as its longer than a few bytes and has a spellingcorrectingness >90
			if percentcorrect >=.9:
				if len(rfile)>30:
					with open(results+"/risk_texts/" + re.sub(".xml", ".txt", name), "w") as text_file:
						_=text_file.write(rfile)
					rmatch = 1
					rs = len(rregex.findall(fulltext))
				else:
					rmatch = 0
					rs=0
			else:
				print("Below spelling threshold: ", percentcorrect)
			#results in dict
			resultsdict= {'Location': "tempzip", 'Filename': name, 'RecordTitle': id, 'Date': date, "Date1": datenum, 'Year': year,
					 'URL': url, 'CompanyName': company.encode('utf-8'), 'NAIC': naics, 'ClassCode': code,
					 'Classification': classic.encode('utf-8'), 'AnrAssetDispIdxNum': anasd, 'rmatch': rmatch, 'risk_words': rs ,
					 'numwords': numwords, 'percentcorrect': percentcorrect}
			resultsdict.update(rdict)
			#write to metadata
			_=writer.writerow(resultsdict)
			print(name, "Written", str(i))
			i+=1







