library( ggplot2 )
library( wesanderson )

baseDirectory <- "./"
dataDirectory <- paste0( baseDirectory, "../Data/Results/" )
segDirectory <- paste0( baseDirectory, "../Data/P56xAlignedSimpleSegmentations/" )

templateIds <- rev( c( "E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56" ) )
templateTimePoints <- rev( c( -1.0 * log( c( 11.5, 13.5, 15.5, 18.5, 23, 33, 47 ) ) ) ) 
normalizedTimePoints = ( templateTimePoints - templateTimePoints[1] ) / ( templateTimePoints[7] - templateTimePoints[1] )

label <- c()
volume <- c()
timePoint <- c()

t <- seq( 11, 1, length.out = 50 )
t <- rev( -1.0 * log( seq( 11.5, 47, length.out = 50 ) ) )
t <- ( t - t[1] ) / ( tail( t, n = 1 ) - t[1] )

for( i in seq.int( length( t ) ) )
  {
  warpedGeomFile <- paste0( dataDirectory, "P56WarpedVolumes_", i-1, ".csv" )
  warpedGeoms <- read.csv( warpedGeomFile )
  label <- c( label, warpedGeoms$Label[1:13] )
  volume <- c( volume, warpedGeoms$VolumeInMillimeters[1:13] )
  timePoint <- c( timePoint, rep( t[i], length( warpedGeoms$Label[1:13] ) ) )
  }

commonLabels <- unique( label )
for( i in seq.int( length( templateIds ) ) )
  {
  template <- antsImageRead( paste0( segDirectory, "P56x", templateIds[i], "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz" ) )
  geoms <- labelGeometryMeasures( template )
  commonLabels <- intersect( commonLabels, geoms$Label )
  }

templateLabel <- c()
templateVolume <- c()
templateTimePoint <- c()

for( i in seq.int( length( templateIds ) ) )
  {
  template <- antsImageRead( paste0( segDirectory, "P56x", templateIds[i], "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz" ) )
  geoms <- labelGeometryMeasures( template )
  templateLabel <- c( templateLabel, commonLabels )
  templateVolume <- c( templateVolume, geoms$VolumeInMillimeters[geoms$Label %in% commonLabels] )
  templateTimePoint <- c( templateTimePoint, rep( normalizedTimePoints[i], length( commonLabels ) ) )
  }



itk_snap_palette = c( "#DC6ED6",
                      "#946EDB",
                      "#F5DEB3",
                      "#FFE4B5",
                      "#23CE32",
                      "#B0C4DE",
                      "#94FC98",
                      "#CE863F",
                      "#006500",
                      "#7C65EE",
                      "#F6A560",
                      "#7C65EE",
                      "#4066E1"
                    )
itk_snap_labels = c( "AH", "SPall", "Pall", "PHy", "p3", "p2", "p1", "M", "PPH", "PH", "PMH", "MH", "tracts" )

warpedVolumesDataFrame <- data.frame( Label = as.factor( label ),
                                      Volume = volume,
                                      TimePoint = timePoint )
templateVolumesDataFrame <- data.frame( Label = as.factor( templateLabel ),
                                        Volume = templateVolume,
                                        TimePoint = templateTimePoint )

warpedVolumesPlot <- ggplot( data = warpedVolumesDataFrame, aes( x = TimePoint, y = Volume ) ) + 
                   geom_point( data = templateVolumesDataFrame, aes( x = TimePoint, y = Volume, fill = Label ), pch = 23, colour = "black", size = 6, alpha = 0.75 ) + 
                   geom_line( aes( group = Label ), colour = "black", alpha = 0.5, size = 0.2 ) + 
                   geom_point( aes( fill = Label ), pch = 21, colour = "black", size = 1 ) + 
                   xlab( "Time point" ) +  
                   ylab( bquote( 'Regional volume ' (mm^3) ) ) +
                   labs( fill = "Region" ) +
                   scale_discrete_manual( "fill", values = itk_snap_palette, labels = itk_snap_labels ) +
                   scale_x_continuous( breaks = normalizedTimePoints, labels = templateIds ) +
                   theme( plot.title = element_text( size = 16, face = "bold" ), 
                          axis.text = element_text( size = 12 ),
                          axis.text.x = element_text( angle = 45, vjust = 0.75 ),
                          axis.title = element_text( size = 13 )
                           ) + 
                   ggtitle( "Warped P56 regional volumes")
ggsave( "./warpedVolumes.pdf", plot = warpedVolumesPlot, width = 8, height = 5, units = "in" )

