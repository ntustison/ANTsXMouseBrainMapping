library( ggplot2 )
library( ANTsR )
library( wesanderson )

baseDirectory <- "./"
scriptsDirectory <- "./"

subjects <- list.dirs( baseDirectory, recursive = FALSE )
timePoints <- c( "Day0", "Day3", "Week1", "Week4", "Week8", "Week20" )
timePointsInDays <- c( 0, 3, 7, 28, 56, 140 )

outputFile <- paste0( scriptsDirectory, "/kk.csv" )

kkDf <- NULL
if( ! file.exists( outputFile ) )
  {
  allSubjects <- c()
  allTimePoints <- c()
  allThicknessMeanValues <- c()
  allIsoThicknessMeanValues <- c()
  wholeHeadDice <- c()
  wholeHeadVolumes <- c()
  hippocampalVolumes <- c()
  hippocampalIsoVolumes <- c()
  corticalVolumes <- c()
  corticalIsoVolumes <- c()
  cerebellarVolumes <- c()
  
  numberNotFinished <- 0
  for( i in seq.int( length( subjects ) ) )
    {
    for( j in seq.int( length( timePoints ) ) )
      {
      files <- list.files( path = paste0( subjects[i], "/", timePoints[j], "/" ), 
                           pattern = ".*cortical_thickness.*", 
                           full.names = TRUE )
      if( length( files ) == 2 )
        {
        parcIsoFile <- sub( "cortical_thickness", "nick_parcellation", files[1] )
        parc_iso <- antsImageRead( parcIsoFile )
        kk_iso <- antsImageRead( files[1] ) * thresholdImage( parc_iso, 1, 1, 1, 0 ) + 
                  antsImageRead( files[1] ) * thresholdImage( parc_iso, 6, 6, 1, 0 )
        kk_iso_mean <- mean( kk_iso[kk_iso != 0] )
        kk_iso_sd <- sd( kk_iso[kk_iso != 0] )

        parcFile <- sub( "cortical_thickness", "nick_parcellation", files[2] )
        parc <- antsImageRead( parcFile )
        kk <- antsImageRead( files[2] ) * thresholdImage( parc, 1, 1, 1, 0 ) + 
              antsImageRead( files[2] ) * thresholdImage( parc, 6, 6, 1, 0 )
        kk_mean <- mean( kk[kk != 0] )
        kk_sd <- sd( kk[kk != 0] )

        geoms <- labelGeometryMeasures( parc )
        geomsIso <- labelGeometryMeasures( parc_iso )

        wholeHead <- thresholdImage( parc, 0, 0, 0, 1 )
        gtWholeHeadFile <- sub( "antspynet_cortical_thickness", "mask", files[2] )
        gtWholeHeadFile <- sub( "Processed", "NiftiReoriented", gtWholeHeadFile )
        gtWholeHead <- antsImageRead( gtWholeHeadFile )
        geoms2 <- labelGeometryMeasures( gtWholeHead )
     
        stats <- labelOverlapMeasures( wholeHead, gtWholeHead )

        allSubjects <- append( allSubjects, basename( subjects[i] ) )
        allTimePoints <- append( allTimePoints, timePointsInDays[j] )
        allThicknessMeanValues <- append( allThicknessMeanValues, kk_mean )
        allIsoThicknessMeanValues <- append( allIsoThicknessMeanValues, kk_iso_mean )
        wholeHeadDice <- append( wholeHeadDice, stats$MeanOverlap[1] )
        wholeHeadVolumes <- append( wholeHeadVolumes, geoms2$VolumeInMillimeters[1] )
        cerebellarVolumes <- append( cerebellarVolumes, geoms$VolumeInMillimeters[4] )

        corticalVolumes <- append( corticalVolumes, geoms$VolumeInMillimeters[1] )
        corticalIsoVolumes <- append( corticalIsoVolumes, geomsIso$VolumeInMillimeters[1] )
        hippocampalVolumes <- append( hippocampalVolumes, geoms$VolumeInMillimeters[6] )
        hippocampalIsoVolumes <- append( hippocampalIsoVolumes, geomsIso$VolumeInMillimeters[6] )

        n4File <- sub( "antspynet_cortical_thickness", "n4", files[2] )
        n4 <- antsImageRead( n4File )
        n4Resampled <- resampleImage( n4, antsGetSpacing( parc_iso ), useVoxels = FALSE, interpType = "linear" )
        n4ResampledFile <- sub( "antspynet_cortical_thickness", "n4_isotropic", files[2] )   
        antsImageWrite( n4Resampled, n4ResampledFile )
        } else {
        numberNotFinished <- numberNotFinished + 1
        }
      }     
    }
  cat( "Number not finished: ", numberNotFinished, "\n" )  

  kkDf <- data.frame( Subject = allSubjects, 
                      TimePoint = allTimePoints,
                      WholeHeadDice = wholeHeadDice,
                      WholeHeadVolume = wholeHeadVolumes,
                      Thickness = allThicknessMeanValues,
                      ThicknessIso = allIsoThicknessMeanValues,
                      CorticalVolume = corticalVolumes,
                      CorticalIsoVolume = corticalIsoVolumes,
                      CerebellarVolume = cerebellarVolumes,
                      HippocampalVolume = hippocampalVolumes,
                      HippocampalIsoVolume = hippocampalIsoVolumes,
                      WholeHeadVolume = wholeHeadVolumes )
  write.csv( kkDf, outputFile, row.names = FALSE )
  } else {
  kkDf <- read.csv( outputFile )
  } 

sex <- rep( "M", length( kkDf$Subject ) )
sex[grepl( "F", kkDf$Subject )] <- 'F'

kkDf$Sex <- sex

returnAverageDataFrame <- function( columnName )
  {
  averageMaleValue <- rep( NA, length( timePoints ) )
  averageFemaleValue <- rep( NA, length( timePoints ) )

  sdMaleValue <- rep( NA, length( timePoints ) )
  sdFemaleValue <- rep( NA, length( timePoints ) )

  for( i in seq.int( length( timePoints ) ) )
    {
    maleValues <- kkDf[kkDf$TimePoint == timePointsInDays[i] & kkDf$Sex == 'M', which( colnames( kkDf ) == columnName )]
    femaleValues <- kkDf[kkDf$TimePoint == timePointsInDays[i] & kkDf$Sex == 'F', which( colnames( kkDf ) == columnName )]
    averageMaleValue[i] <- mean( maleValues )
    averageFemaleValue[i] <- mean( femaleValues )
    sdMaleValue[i] <- sd( maleValues )
    sdFemaleValue[i] <- sd( femaleValues )
    }

  localDataFrame <- data.frame( TimePoint = c( timePointsInDays, timePointsInDays ),
                                 Sex = c( rep( 'Male', length( timePointsInDays ) ), rep( 'Female', length( timePointsInDays ) ) ),
                                 AverageValue = c( averageMaleValue, averageFemaleValue ),
                                 SdValue = c( sdMaleValue, sdFemaleValue ) )
  return( localDataFrame )
  }

colorValues <- c( "NavyBlue", "Orange" )

dicePlot <- ggplot( data = kkDf ) + 
              geom_histogram( aes( x = WholeHeadDice ), color = "black", fill = "Orange", alpha = 0.75 ) + 
              geom_vline( aes( xintercept = mean( WholeHeadDice ) ), color = "NavyBlue", linetype = "dashed", label.size = 0.1, size = 1.25 ) + 
              scale_x_continuous( limits = c( 0.8, 1.0 ) ) +
              theme_minimal() + 
              xlab( "Dice overlap" ) + 
              ylab( "" ) + 
              geom_label( aes( label = paste0( "Mean = ", round( mean( WholeHeadDice ), digits = 2 ) ), x = 0.95, y = 16 ), color = "NavyBlue" ) + 
              ggtitle( "Whole brain extraction" )
ggsave( paste0( scriptsDirectory, "diceWholeBrain.pdf" ), dicePlot, width = 5, height = 3 )

kkThkDf <- returnAverageDataFrame( 'Thickness' )
kkThkDfIso <- returnAverageDataFrame( 'ThicknessIso' )
kkThk <- rbind( kkThkDf, kkThkDfIso )
kkThk$Type <- c( rep( "Anisotropic", nrow( kkThkDf ) ), rep( "Isotropic", nrow( kkThkDfIso ) ) )

kkPlot <- ggplot( kkThk, aes( x = TimePoint, y = AverageValue, colour = Sex, shape = Type ) ) + 
          geom_line( linetype = "dashed", alpha = 0.75 ) +
          geom_point() + 
          geom_errorbar( aes( ymin = AverageValue-2*SdValue, ymax = AverageValue+2*SdValue ), linetype = "solid", alpha = 0.5, width = 4 ) + 
          geom_label( aes( label = "Isotropic", x = 80, y = 1.35 ), color = "NavyBlue", label.size = 0.1, size = 3 ) + 
          geom_label( aes( label = "Anisotropic", x = 80, y = 1.0 ), color = "NavyBlue", label.size = 0.1, size = 3 ) + 
          ggtitle( "" ) + 
          theme_minimal() + 
          xlab( "Age (days)" ) + 
          ylab( "Cortical thickness (mm)" ) + 
          scale_x_continuous( breaks = timePointsInDays ) +
          scale_shape_manual( values = c( 1, 5 ) ) + 
          scale_colour_manual( values = colorValues ) +
          guides( shape = "none" ) +
          theme( legend.position = "right" )
ggsave( paste0( scriptsDirectory, "kkPlot.pdf" ), kkPlot, width = 5, height = 3 )

corticoDf <- returnAverageDataFrame( 'CorticalVolume' )
corticoDfIso <- returnAverageDataFrame( 'CorticalIsoVolume' )
cortico <- rbind( corticoDf, corticoDfIso )
cortico$Type <- c( rep( "Anisotropic", nrow( corticoDf ) ), rep( "Isotropic", nrow( corticoDfIso ) ) )

corticoPlot <- ggplot( cortico, aes( x = TimePoint, y = AverageValue, colour = Sex, shape = Type ) ) + 
          geom_line( linetype = "dashed", alpha = 0.75 ) +
          geom_point() + 
          geom_errorbar( aes( ymin = AverageValue-2*SdValue, ymax = AverageValue+2*SdValue ), linetype = "solid", alpha = 0.5, width = 4 ) + 
          # geom_label( aes( label = "Isotropic", x = 80, y = 1.35 ), color = "NavyBlue", label.size = 0.1, size = 3 ) + 
          # geom_label( aes( label = "Anisotropic", x = 80, y = 1.0 ), color = "NavyBlue", label.size = 0.1, size = 3 ) + 
          ggtitle( "" ) + 
          theme_minimal() + 
          xlab( "Age (days)" ) + 
          ylab( "Cortical volume (ml)" ) + 
          scale_x_continuous( breaks = timePointsInDays ) +
          scale_shape_manual( values = c( 1, 5 ) ) + 
          scale_colour_manual( values = colorValues ) +
          guides( shape = "none" ) +
          theme( legend.position = "right" )
ggsave( paste0( scriptsDirectory, "corticoPlot.pdf" ), corticoPlot, width = 5, height = 3 )

hippoDf <- returnAverageDataFrame( 'HippocampalVolume' )
hippoDfIso <- returnAverageDataFrame( 'HippocampalIsoVolume' )
hippo <- rbind( hippoDf, hippoDfIso )
hippo$Type <- c( rep( "Anisotropic", nrow( hippoDf ) ), rep( "Isotropic", nrow( hippoDfIso ) ) )

hippoPlot <- ggplot( hippo, aes( x = TimePoint, y = AverageValue, colour = Sex, shape = Type ) ) + 
          geom_line( linetype = "dashed", alpha = 0.75 ) +
          geom_point() + 
          geom_errorbar( aes( ymin = AverageValue-2*SdValue, ymax = AverageValue+2*SdValue ), linetype = "solid", alpha = 0.5, width = 4 ) + 
          # geom_label( aes( label = "Isotropic", x = 80, y = 1.35 ), color = "NavyBlue", label.size = 0.1, size = 3 ) + 
          # geom_label( aes( label = "Anisotropic", x = 80, y = 1.0 ), color = "NavyBlue", label.size = 0.1, size = 3 ) + 
          ggtitle( "" ) + 
          theme_minimal() + 
          xlab( "Age (days)" ) + 
          ylab( "Hippocampal volume (ml)" ) + 
          scale_x_continuous( breaks = timePointsInDays ) +
          scale_shape_manual( values = c( 1, 5 ) ) + 
          scale_colour_manual( values = colorValues ) +
          guides( shape = "none" ) +
          theme( legend.position = "right" )
ggsave( paste0( scriptsDirectory, "hippoPlot.pdf" ), hippoPlot, width = 5, height = 3 )
