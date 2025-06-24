library( ggplot2 )

baseDirectory <- "./"

convergenceLogFile <- paste0( baseDirectory, "optimize_velocity_field.log" )
convergenceLines <- readLines( convergenceLogFile )

convergenceValues <- c()
integrationValues <- vector( mode = 'list', 11 )
for( i in seq.int( length( convergenceLines ) ) )
  {
  if( grepl( "Composition", convergenceLines[i] ) ) 
    {
    convergence <- as.double( strsplit( convergenceLines[i], " " )[[1]][5] )
    convergenceValues <- append( convergenceValues, convergence )
    }
  else if( grepl( "integration point", convergenceLines[i] ) )
    {
    integrationPoint <- strsplit( convergenceLines[i], " " )[[1]][5]
    integrationPoint <- round( as.double( sub( ":", "", integrationPoint ) ) * 10 ) + 1
    integrationValue <- strsplit( convergenceLines[i], " = " )[[1]][3]
    integrationValues[[integrationPoint]] <- c( integrationValues[[integrationPoint]], as.double( integrationValue ) )
    }
  }

numberOfIterationsToPlot <- 125

integrationArray <- c()
integrationIds <- c()
for( i in seq.int( 11 ) )
  {
  integrationArray <- c( integrationArray, integrationValues[[i]][1:numberOfIterationsToPlot] )
  integrationIds <- c( integrationIds, rep( paste0( "Integration point ", i ), numberOfIterationsToPlot ) )
  }

convergenceDataFrame <- data.frame( Iteration = seq.int( 1, numberOfIterationsToPlot ),
                                    Error = convergenceValues[1:numberOfIterationsToPlot] )
integrationDataFrame <- data.frame( IntegrationError = integrationArray,
                                    IntegrationPoint = factor( integrationIds, levels = c( "Integration point 0", 
                                                                                              "Integration point 1", 
                                                                                              "Integration point 2", 
                                                                                              "Integration point 3", 
                                                                                              "Integration point 4", 
                                                                                              "Integration point 5", 
                                                                                              "Integration point 6", 
                                                                                              "Integration point 7", 
                                                                                              "Integration point 8", 
                                                                                              "Integration point 9", 
                                                                                              "Integration point 10", 
                                                                                              "Integration point 11"
                                                                                            ) ),
                                    Iteration = rep( seq.int( 1, numberOfIterationsToPlot ), 11 ) )
convergencePlot <- ggplot( data = convergenceDataFrame, mapping = aes( x = Iteration, y = Error ) ) + 
                   geom_point( colour = "black", size = 1 ) + 
                   geom_line( colour = "black", size = 1 ) + 
                   xlab( "Iteration" ) + 
                   ylab( "Total distance error (mm)") +
                   theme( plot.title = element_text( size = 16, face = "bold" ), 
                          axis.text = element_text( size = 12 ),
                          axis.title = element_text( size = 13, face = "bold" ),
                          legend.title=element_blank() ) + 
                   ggtitle( "Overall convergence")
ggsave( "./velocityFieldTotalConvergence.pdf", plot = convergencePlot, width = 5, height = 8, units = "in" )

convergencePlot <- ggplot() + 
                   geom_line( data = integrationDataFrame, mapping = aes( x = Iteration, y = IntegrationError, colour = IntegrationPoint ) ) +
                   geom_point( data = integrationDataFrame, mapping = aes( x = Iteration, y = IntegrationError, colour = IntegrationPoint ), size = 1 ) +
                   xlab( "Iteration" ) + 
                   ylab( "Median distance error (mm)") +
                   theme( plot.title = element_text( size = 16, face = "bold" ), 
                          axis.text = element_text( size = 12 ),
                          axis.title = element_text( size = 13, face = "bold" ),
                          legend.title=element_blank() ) + 
                   ggtitle( "Per integration point" )
ggsave( "./velocityFieldIntegrationConvergence.pdf", plot = convergencePlot, width = 6.5, height = 8, units = "in" )
