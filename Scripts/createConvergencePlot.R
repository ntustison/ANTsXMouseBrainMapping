library( ggplot2 )

baseDirectory <- "./"

convergenceLogFile <- paste0( baseDirectory, "optimize_velocity_field.log" )
convergenceLines <- readLines( convergenceLogFile )

convergenceValues <- c()
for( i in seq.int( length( convergenceLines ) ) )
  {
  if( grepl( "Composition", convergenceLines[i] ) ) 
    {
    convergence <- strsplit( convergenceLines[i], " " )[[1]][5]
    convergenceValues <- append( convergenceValues, convergence )
    }
  }
convergenceValues <- as.double( convergenceValues )[1:125]

convergenceDataFrame <- data.frame( Iteration = seq.int(1, length( convergenceValues ) ),
                                    Error = convergenceValues )
convergencePlot <- ggplot( data = convergenceDataFrame, mapping = aes( x = Iteration, y = Error ) ) + 
                   geom_point( colour = "black" ) + 
                   xlab( "Iteration" ) + 
                   ylab( "Point Distance Error (mm)") +
                   theme( plot.title = element_text( size = 16, face = "bold" ), 
                          axis.text = element_text( size = 12 ),
                          axis.title = element_text( size = 13, face = "bold" ) ) + 
                   ggtitle( "Convergence of velocity field optimization")
ggsave( "./velocityFieldConvergence.pdf", plot = convergencePlot, width = 8, height = 5, units = "in" )
