
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
load('future_paragraphs_preparations_27JUNE2020.RData')

#STM40
stm5 <- stm(out$documents, out$vocab, data = out$meta, 
             K = 5, prevalence =  ~s(Year))

effects5 <- estimateEffect(1:5 ~ s(Year),
                            stm5, metadata = out$meta)

save.image('stm5_futurepara.RData',
           compress = TRUE)
