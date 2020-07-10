
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
stm50 <- stm(out$documents, out$vocab, data = out$meta, 
             K = 50, prevalence =  ~s(Year))

effects50 <- estimateEffect(1:50 ~ s(Year),
                            stm50, metadata = out$meta)

save.image('stm50_futurepara_FUTUREONLY.RData',
           compress = TRUE)
