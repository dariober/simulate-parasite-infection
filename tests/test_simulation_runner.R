library(testthat)

context("Test functions")

source('../R/simulation_runner.R')

test_that("Can simulate and plot", {
    
    parasitePops <- list(R= list(resistance= 0.05, repr_rate= 1.5, count= 100, transmissibility= 0.9), 
                       S= list(resistance= 0.05, repr_rate= 2.2, count= 100, transmissibility= 0.9))

    events <- c(rep('REPRODUCE', 20),
                rep(c('TREATMENT', rep('REPRODUCE', 3)), 4),
                'MOSQUITO_BITE',
                rep(c('TREATMENT', rep('REPRODUCE', 3)), 4)
               )

    hh <- simulation_runner(parasitePops, events, path= '..')
    expect_true(nrow(hh) > 10)

    gg <- simulation_plotter(hh)
    expect_true('ggplot' %in% class(gg))
})

test_that("Can build events", {
    events <- eventBuilder('RTM')
    expect_equal(c('REPRODUCE', 'TREATMENT', 'MOSQUITO_BITE'), events)

    events <- eventBuilder('R, R, T, M')
    expect_equal(c('REPRODUCE', 'REPRODUCE', 'TREATMENT', 'MOSQUITO_BITE'), events)

    events <- eventBuilder('')
    expect_equal(0, length(events))

    events <- eventBuilder(',,foobar')
    expect_equal(0, length(events))

    events <- eventBuilder('10R3T2MM,R, T')
    expect_equal(c('REPRODUCE', 'REPRODUCE', 'REPRODUCE', 'TREATMENT', 'TREATMENT', 'MOSQUITO_BITE', 'MOSQUITO_BITE', 'REPRODUCE', 'TREATMENT'), events)

    events <- eventBuilder('R1')
    expect_equal(c('REPRODUCE'), events)

    events <- eventBuilder('R')
    expect_equal(c('REPRODUCE'), events)

    events <- eventBuilder('RR')
    expect_equal(c('REPRODUCE', 'REPRODUCE'), events)

    events <- eventBuilder('RRR3')
    expect_equal(rep('REPRODUCE', 5), events)

    events <- eventBuilder('RRR3T2')
    expect_equal(c(rep('REPRODUCE', 5), 'TREATMENT', 'TREATMENT'), events)

    expect_error(eventBuilder('RRR300', 100))
})
