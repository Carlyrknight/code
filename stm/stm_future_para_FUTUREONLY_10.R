
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
stm10 <- stm(out$documents, out$vocab, data = out$meta, 
             K = 10, prevalence =  ~s(Year))

effects10 <- estimateEffect(1:10 ~ s(Year),
                            stm10, metadata = out$meta)

save.image('stm10_futurepara_FUTUREONLY.RData',
           compress = TRUE)
