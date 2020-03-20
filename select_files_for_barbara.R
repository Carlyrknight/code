---
title: "Select Files for Barbara"
author: "Carly Knight"
date: "3/17/2020"
output: html_document
---
  
library(tidyverse)
library(dplyr)
  
metadata<- read.csv("/Users/carlyknight/Documents/Data/Annual Report/report_paragraphs/future_texts/metadata_futureperfect.csv")

#select companies with a lot of observations
companypanels<-metadata %>%
  filter(Year >=1930) %>%
  group_by(CompanyName)%>%
  summarize(N = n())%>%
  filter(N>=30)

#randomly select 30
selected<-as_tibble(sample(companypanels$CompanyName, size = 30, replace = F))
colnames(selected)<- "CompanyName"

#merge back in
selected_data <- selected%>%
  left_join(metadata)%>%
  select(CompanyName, Filename, Year) %>%
  mutate(Filename = str_replace(Filename, ".xml", ".txt"))
  
#get list of all files
setwd("~/Documents/Data/Annual Report/report_paragraphs/future_texts/")

list_of_files <- list.files(pattern = "*.txt")

all_files <- list_of_files %>% 
  map_chr(~ read_file(.)) %>% 
  tibble(text = .)

all_files$Filename<-list_of_files

#select files 
selected_text <- selected_data %>%
  left_join(all_files) %>%
  mutate(CompanyName = as.character((CompanyName)))%>%
  mutate(CompanyName = str_replace(CompanyName, "b'", ""))%>%
  mutate(CompanyName = str_replace(CompanyName, "'", ""))

#group by company
selected_text_company <- selected_text %>%
  mutate(text2 = paste("YEAR: ", Year, text, sep = " \n "))%>%
  arrange(CompanyName, Year)%>%
  group_by(CompanyName) %>% 
  mutate(text2_time = paste0(text2, collapse = "\n")) 

selected_text_company <- unique(selected_text_company %>%
  select(CompanyName, text2_time))

setwd("/Users/carlyknight/Dropbox/PROJECTS/ConceptionsofRisk/filesforbarbara/30_companies_over_time_2/")

for (row in 1:nrow(selected_text_company)){
  
  name = selected_text_company[row, 'CompanyName']
  
  textlines <- as.character(selected_text_company[row, 'text2_time'])

  writeLines(text= textlines , paste("/Users/carlyknight/Dropbox/PROJECTS/ConceptionsofRisk/filesforbarbara/30_companies_over_time_2/", name, ".txt", sep = ""))
  
  
  }
  
writeLines(text= textlines , paste("/Users/carlyknight/Dropbox/PROJECTS/ConceptionsofRisk/filesforbarbara/30_companies_over_time_2/", name, ".txt", sep = ""))

# #write to files
# setwd("/Users/carlyknight/Dropbox/PROJECTS/ConceptionsofRisk/filesforbarbara/30_companies_over_time/")
# 
# for (row in 1:nrow(selected_text)){
#   
# print(row)
#   
# name<- paste(selected_text[row, 'CompanyName'], selected_text[row, 'Year'], selected_text[row, 'Filename'], sep = "_")
# 
# textlines <- as.character(selected_text[row, 'text'])
# 
# writeLines(textlines , name)
#   
# }

