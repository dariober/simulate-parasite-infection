library(shiny)

ui <- fluidPage(

    tags$style(HTML(".js-irs-0 .irs-single, .js-irs-0 .irs-bar-edge, .js-irs-0 .irs-bar {background: green}")),
    tags$style(HTML(".js-irs-1 .irs-single, .js-irs-1 .irs-bar-edge, .js-irs-1 .irs-bar {background: green}")),
    tags$style(HTML(".js-irs-2 .irs-single, .js-irs-2 .irs-bar-edge, .js-irs-2 .irs-bar {background: green}")),
    tags$style(HTML(".js-irs-3 .irs-single, .js-irs-3 .irs-bar-edge, .js-irs-3 .irs-bar {background: darkorange}")),
    tags$style(HTML(".js-irs-4 .irs-single, .js-irs-4 .irs-bar-edge, .js-irs-4 .irs-bar {background: darkorange}")),
    tags$style(HTML(".js-irs-5 .irs-single, .js-irs-5 .irs-bar-edge, .js-irs-5 .irs-bar {background: darkorange}")),

    titlePanel("Simulate parasite dynamic"),

    sidebarLayout(
        sidebarPanel(
            sliderInput(inputId = "repr_rate_1",
                      label = "Pop 1 | Reproductive rate",
                      min = 0,
                      max = 5,
                      step = 0.02,
                      value = 1.5),

            sliderInput(inputId = "resistance_1",
                      label = "Pop 1 | Drug resistance",
                      min = 0,
                      max = 1,
                      step = 0.02,
                      value = 0.9),

            sliderInput(inputId = "transmissibility_1",
                      label = "Pop 1 | Transmissibility",
                      min = 0,
                      max = 1,
                      step = 0.02,
                      value = 0.9),

            sliderInput(inputId = "repr_rate_2",
                      label = "Pop 2 | Reproductive rate",
                      min = 0,
                      max = 5,
                      step = 0.02,
                      value = 2),

            sliderInput(inputId = "resistance_2",
                      label = "Pop 2 | Drug resistance",
                      min = 0,
                      max = 1,
                      step = 0.02,
                      value = 0.1),
                     
            sliderInput(inputId = "transmissibility_2",
                      label = "Pop 2 Transmissibility",
                      min = 0,
                      max = 1,
                      step = 0.02,
                      value = 0.9),
            
            textAreaInput("events", 
                          "Events", 
                          value= "R20, T, RRR, T, RRR, T, RRR, T, RRR, M\nR20, T, RRR, T, RRR, T, RRR, T, RRR",
                          height= '10%',
                          resize= 'both',
                          rows= 10),

            actionButton("run", "Run simulation")
        ),

        mainPanel(
            plotOutput(outputId = "historyPlot")
        )
    )
)

server <- function(input, output) {
    
    source('../R/simulation_runner.R')
    
    hh <- eventReactive(input$run, {
        parasitePops <- list(
            P1= list(count= 100, resistance= input$resistance_1, repr_rate= input$repr_rate_1, transmissibility= input$transmissibility_1),
            P2= list(count= 100, resistance= input$resistance_2, repr_rate= input$repr_rate_2, transmissibility= input$transmissibility_2)
        )

        events <- eventBuilder(input$events)
        validate(
            need(length(events) > 0, 'There is no event to simulate!')
        )

        hh <- simulation_runner(parasitePops, events, path= '..')
        return(hh)
    })

    output$historyPlot <- renderPlot({
        gg <- simulation_plotter(hh())
        return(gg)
    })
}

shinyApp(ui = ui, server = server)
