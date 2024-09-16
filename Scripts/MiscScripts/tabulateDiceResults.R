library( ggplot2 )
library( ANTsR )
library( wesanderson )
library( reshape2 )

itkColors <- c( rgb( 1, 0, 0 ), 
                rgb( 0, 1, 0 ),
                rgb( 0, 0, 1 ),
                rgb( 1, 1, 0 ),
                rgb( 1, 0, 1 ),
                rgb( 0, 1, 1 ) )
regions <- c( "CerebralCortex", 
              "CerebralNuclei",
              "BrainStem",
              "Cerebellum",
              "HippocampalFormation",
              "MainOlfactoryBulb" )                

baseDirectory <- "./"
dice <- read.csv( paste0( baseDirectory, "dice_overlap.csv" ) )

dice <- dice[dice$Day != "ex_vivo",]
dice <- dice[dice$Registration != "Intensity only",]

dice$Registration[dice$Registration == "Intensity (brain-extracted)"] <- "Intensity only"
dice$Registration[dice$Registration == "Intensity with parcellation"] <- "With parcellation"

dice <- dice[dice$All > 0.1,]
dice$All <- NULL
dice$X <- NULL 
dice_melt <- reshape2::melt( dice, value.name = "Dice", variable.name = "Region" )
dice_melt$Region <- factor( dice_melt$Region, levels = regions )

dicePlot <- ggplot( data = dice_melt, aes( x = Registration, y = Dice, fill = Region ) ) + 
              geom_boxplot() + 
              xlab( "" ) +
              ylab( "Dice overlap" ) +
              ylim( c( 0.6, 1.0 ) ) + 
              ggtitle( "Normalization to AllenCCFv3" ) + 
              scale_fill_manual( name = "Regions", labels = regions, values = itkColors ) + 
              theme( axis.text.x = element_text( angle = 0, vjust = 0.5 ) )
ggsave( paste0( "~/Desktop/diceAllenCCFv3.png" ), dicePlot, width = 7, height = 4 )

######################################################


# baseDirectory <- "./"
# dice <- read.csv( paste0( baseDirectory, "dice_overlap.csv" ) )

# dice <- dice[dice$Day != "ex_vivo",]
# dice <- dice[dice$Registration != "Intensity only",]
# dice <- dice[dice$All > 0.1,]
# dice$X <- NULL 
# dice <- dice[,1:4]

# dicePlot <- ggplot( data = dice, aes( x = Day, y = All, fill = Registration ) ) + 
#               geom_boxplot() + 
#               xlab( "" ) +
#               ylab( "Dice overlap" ) +
#               ylim( c( 0.6, 1.0 ) ) + 
#               ggtitle( "Normalization to AllenCCFv3" ) + 
#               theme( axis.text.x = element_text( angle = 45, vjust = 0.5 ) )
# ggsave( paste0( "~/Desktop/diceAllenCCFv3_2.png" ), dicePlot, width = 7, height = 4 )

