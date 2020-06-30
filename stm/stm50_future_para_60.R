
title: "Worker Topic Models: STM60"
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
stm60 <- stm(out$documents, out$vocab, data = out$meta, 
             K = 60, prevalence =  ~s(Year))

effects60 <- estimateEffect(1:60 ~ s(Year),
                            stm60, metadata = out$meta)

save.image('stm60_futurepara.RData',
           compress = TRUE)
