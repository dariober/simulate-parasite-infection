library(reticulate)
library(data.table)
library(ggplot2)

use_python(python= py_config()$python)

eventBuilder <- function(event_str, max_size= 1000) {
    EVENTS <- list(R= 'REPRODUCE', T= 'TREATMENT', M= 'MOSQUITO_BITE')

    x <- sub('^\\d+', '', event_str)
    x <- gsub('[^0-9RTM]', '', x)

    x <- strsplit(event_str, '')[[1]]
    if (length(x) == 0) {
        return(c())
    } 
    
    events <- c()
    times <- c()
    for(z in x) {
        if(z %in% names(EVENTS)) {
            events <- append(events, paste(times, collapse= ''))
            events <- append(events, z)
            times <- c()
        } else if(z %in% 0:9) {
            times <- append(times, z)
        }
    }
    events <- append(events, paste(times, collapse= ''))
    events <- events[!events %in% c('0', '')]
    if(length(events) == 0) {
        return(c())
    }
    events_full <- c()
    for(z in events) {
        if(z %in% names(EVENTS)) {
            events_full <- append(events_full, EVENTS[[z]])
        } else {
            if(length(events_full) == 1) {
                prev_event <- events_full[1]
                events_full <- c()
            } else {
                prev_event <- events_full[length(events_full)]
                events_full <- events_full[1:(length(events_full) - 1)]
            }
            z <- as.numeric(z)
            if(z > max_size) {
                stop(sprintf('Max number of events must be < %s', max_size))
            }

            events_full <- append(events_full, rep(prev_event, as.numeric(z)))
            if(length(events_full) > max_size) {
                stop(sprintf('Max number of events must be < %s', max_size))
            }
        }
    }
    return(events_full)
}

simulation_runner <- function(parasitePops, events, max_size= 1e7, blood_dilution= 1e-4, path= '..') {
    # parasitePops: named list of parasite populations to start the simulation.
    # The default value is given as example
    # path: Path to python module 'simulate_infection'
    # -------------------------------------------------------------------------

    makeParasitePops <- function(parasitePops, path) {
        # Turn the list parasitePops in a dictionary suitable for running the simulation
        
        parasite <- import_from_path('simulate_infection.parasite', path= path)
        
        parasiteDict <- list() 
        for(p in names(parasitePops)) {
            pp <- parasitePops[[p]]
            parasiteDict[[p]] <- parasite$ParasitePop(count= pp$count, resistance= pp$resistance, repr_rate= pp$repr_rate, transmissibility= pp$transmissibility)
        }
        return(dict(parasiteDict))
    }

    hs <- import_from_path('simulate_infection.host', path= path)
    infx <- import_from_path('simulate_infection.infection', path= path)

    parasitePops <- makeParasitePops(parasitePops, path)
    infection <- infx$Infection(parasitePops, max_size= max_size)
    host <- hs$Host(infection= infection)

    for(event in events) {
        if(event == 'REPRODUCE') {
            host$reproduce_parasites(times= 1)
        } else if (event == 'TREATMENT') {
            host$apply_treatment()
        } else if (event == 'MOSQUITO_BITE') {
            host$mosquito_bite(blood_dilution= blood_dilution)
        } else {
            stop(sprintf('Unexpected event: "%s"', event))
        }
    }

    hh <- as.data.table(host$to_dataframe())
    last_tp <- max(hh$time_point)
    hh <- hh[count > 0]
    return(hh)
}

simulation_plotter <- function(history, cex_size= 2) {

    ylabeller <- function(breaks) {
        labs <- format(round(breaks/1000), big.mark= ',', scientific=FALSE)
        return(labs)
    }

    xlabeller <- function(breaks) {
        labs <- sprintf('%.0f', breaks)
        return(labs)
    }
    last_tp <- max(history$time_point)
    history <- history[count > 0]

    legend_key <- unique(history[, list(key= sprintf('Resistance: %.2f\nRepr. rate:   %.2f', c(resistance), c(repr_rate))), by= pop_name])

    gg <- ggplot(data= history, aes(x= time_point, y= count, colour= pop_name)) +
        geom_point(size= 0.25 * cex_size) +
        geom_point(data= history[, .SD[which.max(time_point)], by= pop_name], size= 2 * cex_size) +
        geom_line(size= 0.5 * cex_size) +
        scale_color_brewer(palette="Dark2", name= '', breaks= legend_key$pop_name, labels= legend_key$key) +
        scale_y_continuous(trans= 'identity', labels= ylabeller, expand= c(0, 0.05)) +
        scale_x_continuous(labels= xlabeller, limits= c(0, last_tp)) +
        coord_cartesian(clip="off") +
        ylab('Parasites x1000') +
        xlab('Time point') +
        theme_classic() +
        theme(legend.position= 'none', text= element_text(size= 10 * cex_size))
    if('MOSQUITO_BITE' %in% history$event) {
        gg <- gg + geom_point(data= unique(history[event == 'MOSQUITO_BITE']), aes(x= time_point, y= 1), colour= 'black', pch= 24, fill= 'black', size= 3 * cex_size)
    }
    if('TREATMENT' %in% history$event) {
        gg <- gg + geom_vline(xintercept= unique(history[event == 'TREATMENT']$time_point)-1, colour= 'grey30', linetype= 'dashed', size= 0.25 * cex_size)
    }
    return(gg)
}
