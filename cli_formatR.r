#!/usr/bin/env Rscript

list.of.packages <- c("formatR")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages, repos="https://cran.ma.imperial.ac.uk/")


args = commandArgs(trailingOnly=TRUE)
formatR::tidy_source(args[1], file=args[1])