#!/bin/bash
#
echo Rscript code/01_pull_ZCTA_INTPT.R 
Rscript code/01_pull_ZCTA_INTPT.R &&
echo Rscript code/02_pull_DNI_latlon.R 
Rscript code/02_pull_DNI_latlon.R &&
echo Rscript code/03_pull_GHI_latlon.R 
Rscript code/03_pull_GHI_latlon.R &&
echo Rscript code/04_pull_DEM_ul_lr_zmean.R
Rscript code/04_pull_DEM_ul_lr_zmean.R
