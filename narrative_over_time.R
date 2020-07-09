library(dplyr)
library(stringr)
library(tidyr)
library(ggplot2)

setwd("/Users/carlyknight/Documents/Data/Annual Report/report_paragraphs/future_text_for_mat/")

#get stats directories
alldirectories <- list.dirs()
statsdirectories<- alldirectories[grepl("Statistics", alldirectories)]

#cycle through files, put them into a list
dimlist<-list()

for (i in statsdirectories){
  year<-str_extract(i, "[0-9]+\\.0")
  dimfile<-paste(i, "/Dimensions_", year, ".dat", sep = "")
  temp<-read.delim(dimfile, header = TRUE, sep="\t") 
  temp$year<- year
  dimlist[[i]]<-temp
}

#rbind list
dimensions <-do.call(rbind, dimlist)

#means
summary<-dimensions %>%
  group_by(year)%>%
  summarize(
    mean_dim2 = mean(Dimension2, na.rm = T),
    mean_dim4 = mean(Dimension4, na.rm =T),
    mean_dim5 = mean(Dimension5, na.rm =T))

#reshape
summarylong<-summary%>%
  gather(key = dimension, value= score, mean_dim2:mean_dim5 )

ggplot(summarylong, aes(x= year, score ))+
  geom_point()+
  facet_wrap(~dimension)+
  theme_minimal()

ggsave("/Users/carlyknight/Dropbox/PROJECTS/ConceptionsofRisk/data/narrativescores.pdf")

#stat <- read.delim(statfile, header = TRUE, sep="\t") 
#zscores <- read.delim(zfile, header = TRUE, sep="\t") 
#dims <- read.delim(dimfile, header = TRUE, sep="\t") 
