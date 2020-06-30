---
title: "Future Paragraphs Data Management"
description: prepares paragraphs for stm analyses
date: "6/22/2020"
output: worker_tbl+ dfm + stm_output
---
  
#clean workspace
rm(list = ls())

#Load packages
library(stm)
library(quanteda)
library(ggplot2)
library(tidyverse)
library(dplyr)
library(stringr)

#set working directory
setwd("~/Documents/Data/Annual Report/report_paragraphs/future_texts_paragraphs")

#create text tibble
futurepara_list_of_files <- list.files(".", pattern = "*.txt")

#create text tibble
list_of_files <- list.files(pattern = "*.txt")

tbl <- list_of_files %>% 
  map_chr(~ read_file(.)) %>% 
  tibble(text = .)

tbl$paragraph_filename<-list_of_files

#read in metadata
metadata<- read.csv(file="/Users/carlyknight/Documents/Data/Annual Report/report_paragraphs/future_texts/metadata_futureperfect_paragraphs.csv", quote="", stringsAsFactors=FALSE)

#rename vars
metadata<-metadata %>%
  dplyr::rename(document_name=Filename)%>%
  mutate(paragraph_filename = paste(str_replace(document_name, ".xml", ""), "_P",  Paragraph, ".txt", sep = ""))

nrow(metadata) 
#1,056,390

#merge metadata + txt files
tbl1 <- left_join(tbl, metadata, by = c("paragraph_filename"))
colnames(tbl1)

#keep full rows
tbl1<-tbl1[complete.cases(tbl1$Year), ]
nrow(tbl1) 
#978189

#select text: select docs with >1930
tbl1<-tbl1 %>%
  dplyr::select(document_name, paragraph_filename, Year, text)%>%
  filter(Year>=1930)

#tokenize for collocations
tbl_tokens <- tokens(tbl1$text, remove_punct = TRUE, remove_separators=TRUE, remove_symbols=TRUE, remove_numbers = TRUE, remove_twitter =TRUE) %>% 
  tokens_tolower() %>%
  tokens_remove(c(stopwords('english')),  min_nchar = 2L,  padding = TRUE)%>%
  tokens_remove('#', valuetype= "regex")

#collocations
coll <- textstat_collocations(tbl_tokens, min_count = 1000)

#combine collocations, remove tokens with 2 or fewer characters 
tbl_tokens <- tokens_compound(tbl_tokens, coll, join = FALSE) %>%
  tokens_remove(min_nchar = 3L)

#convert to dfm: stem 
dfm_w <- tbl_tokens %>% dfm(stem=TRUE) 

#remove low frequency
dfm_w1<-dfm_trim(dfm_w, min_termfreq = 15)
topfeatures(dfm_w1, 500)

#select variables to model (first turn assets into quartiles)
to_model <- tbl1 %>% 
  select(Year, paragraph_filename)

#create STM objecttbl1$
docvars(dfm_w1) <- to_model
out <- convert(dfm_w1, to = 'stm')

rm(tbl1, coll, tbl, tbl_tokens, dfm_w, dfm_w1, to_model)

save.image('/Users/carlyknight/Dropbox/PROJECTS/ConceptionsofRisk/data/stm/future_paragraphs_preparations_27JUNE2020.RData',
           compress = TRUE)

