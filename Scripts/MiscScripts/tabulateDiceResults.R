library( ggplot2 )
library( ANTsR )
library( wesanderson )
library( reshape2 )

baseDirectory <- "./"
dice <- read.csv( paste0( baseDirectory, "dice_overlap.csv" ) )

dice <- dice[dice$Day != "ex_vivo",]
dice <- dice[dice$Registration != "Intensity only",]
dice <- dice[dice$All > 0.1,]
dice$All <- NULL
dice$X <- NULL 
dice_melt <- reshape2::melt( dice, value.name = "Dice", variable.name = "Region" )

colorValues <- c( "NavyBlue", "Orange" )

dicePlot <- ggplot( data = dice_melt, aes( x = Registration, y = Dice, fill = Region ) ) + 
              geom_boxplot() + 
              xlab( "" ) +
              ylab( "Dice overlap" ) +
              ylim( c( 0.6, 1.0 ) ) + 
              ggtitle( "Normalization to AllenCCFv3" ) + 
              theme( axis.text.x = element_text( angle = 45, vjust = 0.5 ) )
ggsave( paste0( "~/Desktop/diceAllenCCFv3.png" ), dicePlot, width = 9, height = 7 )

######################################################


baseDirectory <- "./"
dice <- read.csv( paste0( baseDirectory, "dice_overlap.csv" ) )

dice <- dice[dice$Day != "ex_vivo",]
dice <- dice[dice$Registration != "Intensity only",]
dice <- dice[dice$All > 0.1,]
dice$X <- NULL 
dice <- dice[,1:4]

dicePlot <- ggplot( data = dice, aes( x = Day, y = All, fill = Registration ) ) + 
              geom_boxplot() + 
              xlab( "" ) +
              ylab( "Dice overlap" ) +
              ylim( c( 0.6, 1.0 ) ) + 
              ggtitle( "Normalization to AllenCCFv3" ) + 
              theme( axis.text.x = element_text( angle = 45, vjust = 0.5 ) )
ggsave( paste0( "~/Desktop/diceAllenCCFv3_2.png" ), dicePlot, width = 9, height = 7 )

