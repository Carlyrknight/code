
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

#setWD
setwd('~/Dropbox/PROJECTS/ConceptionsofRisk/data/stm')

#load
load('future_paragraphs_preparations_futureonly_7JULY2020.RData')

#STM10
stm70 <- stm(out$documents, out$vocab, data = out$meta, 
             K = 70, prevalence =  ~s(Year))

effects70 <- estimateEffect(1:70 ~ s(Year),
                            stm70, metadata = out$meta)

save.image('stm70_futurepara_FUTUREONLY.RData',
           compress = TRUE)
