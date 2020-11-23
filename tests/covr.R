library(covr)
setwd('tests')
xcov <- file_coverage(source_files= '../R/simulation_runner.R', test_files=  c('test_simulation_runner.R'))
codecov(coverage= xcov, token= '853ba810-ff8b-4cc2-9834-3f3817687feb') # Get token from https://app.codecov.io/gh/dariober/simulate-parasite-infection/settings
