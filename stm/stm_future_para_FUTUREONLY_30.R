
title: "Worker Topic Models: STM50"
date: "1/21/20"
output: stm matrix

################
#STM
###############
rm(list = ls())

#Load packages
library(stm)
library(quanteda)


#######
#set K
#######

k=30

######
#run
#######

#setWD
setwd('~/Dropbox/PROJECTS/ConceptionsofRisk/data/stm')

#load
load('future_paragraphs_preparations_futureonly_7JULY2020.RData')

#STM30
stm30 <- stm(out$documents, out$vocab, data = out$meta, 
             K = k, prevalence =  ~s(Year))

effects30 <- estimateEffect(1:k ~ s(Year),
                            stm30, metadata = out$meta)

filename = paste("stm", k, "_futurepara_FUTUREONLY.RData", sep = "")
save.image(filename,
           compress = TRUE)
