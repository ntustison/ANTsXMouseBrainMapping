library( rmarkdown )
library( ggplot2 )

stitchedFile <- "stitched.md"

rmdFiles <- c( "format.md",
               "titlePage.md",
               "abstract.md",
               "intro.md",
               "introAnts.md",
               "resultsAllen.md",
               "resultsDevCCF.md",
               "resultsKK.md",
               "discussion.md",
               "methods.md",
               "data_availability.md",
               "acknowledgments.md",
               "author_contributions.md",
               "references.md"
             )

for( i in 1:length( rmdFiles ) )
  {
  cat( rmdFiles[i] )
  if( i == 1 )
    {
    cmd <- paste( "cat", rmdFiles[i], ">", stitchedFile )
    } else {
    cmd <- paste( "cat", rmdFiles[i], ">>", stitchedFile )
    }
  system( cmd )
  }

cat( '\n Pandoc rendering', stitchedFile, '\n' )
render( stitchedFile, pdf_document( number_sections = TRUE, pandoc_args = "--variable=subparagraph" ) )
render( stitchedFile, latex_document() )

