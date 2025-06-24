library( ggplot2 )
library( ANTsR )
library( reshape2 )

synOverlap <- read.csv("dev_ccf_dice_pairwise_syn_overlap.csv")
synOverlap$X <- NULL
synOverlap$Label <- NULL

vfOverlap <- read.csv("dev_ccf_dice_velocity_flow_overlap.csv")
vfOverlap$X <- NULL
vfOverlap$Label <- NULL

timePoints <- c( "P56", "P14", "P04", "E18.5", "E15.5", "E13.5", "E11.5" )

syn <- rep( 0, length( timePoints ) )
syn[1] <- synOverlapAll[1,1]
syn[7] <- synOverlapAll[1,12]
vf <- rep( 0, length( timePoints ) )
vf[1] <- vfOverlapAll[1,1]
vf[7] <- vfOverlapAll[1,12]

for( i in seq.int( 2, 6 ) )
  {
  syn[i] <- 0.5 * ( synOverlapAll[1,2*(i-1)] + synOverlapAll[1,2*(i-1)+1] )
  vf[i] <- 0.5 * ( vfOverlapAll[1,2*(i-1)] + vfOverlapAll[1,2*(i-1)+1] )
  }

devData <- data.frame( Pipeline = c( rep( 'SyN', length( timePoints ) ),
                                     rep( 'Velocity flow', length( timePoints ) ) ),
                       TimePoint = c( timePoints, timePoints ),
                       Dice = c( syn, vf )
                     )

devPlot <- ggplot( devData ) + 
           geom_col( aes( x = TimePoint, y = Dice, fill = Pipeline, group = Pipeline ), position = "dodge" ) + 
           xlab( "Developmental time point" ) +
           ylab( "Dice overlap" ) +
           ggtitle( "Pairwise SyN vs. velocity flow model" ) + 
           theme( plot.title = element_text( size = 16, face = "bold" ), 
                  axis.text = element_text( size = 12 ),
                  axis.title = element_text( size = 13, face = "bold" ),
                  legend.title = element_blank())
ggsave( "./devCcfDiceOverlap.pdf", plot = devPlot, width = 8, height = 4, units = "in" )
