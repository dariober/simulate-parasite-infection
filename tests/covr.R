library(covr)
setwd('tests')
xcov<- file_coverage(source_files= '../R/simulation_runner.R', test_files=  c('test_simulation_runner.R'))
codecov(coverage= xcov)
