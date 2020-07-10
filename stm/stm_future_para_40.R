
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

#STM60
stm40 <- stm(out$documents, out$vocab, data = out$meta, 
             K = 40, prevalence =  ~s(Year) + quantile_rank + NAIC_broad)

effects40 <- estimateEffect(1:40 ~ s(Year)*quantile_rank + NAIC_broad,
                            stm60, metadata = out$meta)

save.image('stm40_futurepara.RData',
           compress = TRUE)