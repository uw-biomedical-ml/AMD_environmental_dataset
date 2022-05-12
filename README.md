This repository contains the code used to generate our environmental data used in the analysis for our paper, "Association of Environmental Factors with Age-Related Macular Degeneration using the Intelligent Research in Sight (IRIS)® Registry." We have provided both our generated data and our source code in hope that it will facilitate future analyses. Refer to the methods section for more detailed explanation of data preparation.

The final data files used in our analysis are located in "final_data/". They are "final_data/ghi_matched_master_cleaned_plus_zcta.tsv" and "final_data/zcta_master_with_pollution.tsv". Files match those used in our analysis to within rounding error. 

- "final_data/zcta_master_with_pollution.tsv" contains each Zip Code Tabulation Area internal point matched to its nearest-neighbor environmental metric in each category. Each ZCTA is given a row in this dataset. This file was used in our analysis to assign environmental exposures to each patient in our study, as patients could be approximately localized to a ZCTA.
- "final_data/ghi_matched_master_cleaned_plus_zcta.tsv" is used to generate high-resolution maps of environmental variables and risk ratios. In this file, each point of measurement for GHI and DNI has been matched to their nearest neighbor for every other environmental variable. This permits plotting up to the resolution of GHI and DNI, our highest-resolution data.

To generate these data files from scratch, run "./code/sh_run_all.sh".

All Environmental Factors Plotted from "final_data/ghi_matched_master_cleaned_plus_zcta.tsv"

![Maps](./figures/all_env_factors_subplots_1e+06.png)


__Notes:__
- The zcta column in final_data/ghi_matched_master_cleaned_plus_zcta.tsv refers to the nearest ZCTA internal point, not necessarily the ZCTA within which the GHI and DNI latitude and longitude point reside.
- Data generated from scratch using this repo is identical to our analysis data, except for latitude and longitude. Largest discrepancy in either of these metrics was on the order of 1e-6.
    - However, due to these small discrepancies, the voronoi diagram package used in the paper (ggvoronoi) could not generate maps at full resolution. We thus used the "ggforce" package to generate the maps in this repo.
- An improvement to the mapping code would map each environmental variable at its native resolution, rather than at GHI resolution. This would actually result in more crisp maps, because the Voronoi cells would be larger with straight lines.



__Citations for Data Sources:__
- ZCTA information (coordinates internal points) obtained from R's Tigris package.
- Elevation information from USGS Lidar Explorer: "https://prd-tnm.s3.amazonaws.com/LidarExplorer/index.html#/"
    - Select "DEM", "Show where DEMs exist?", "more info", and click to download 1 arc-second data.
- GHI and DNI information from nsrdb viewer: "https://maps.nrel.gov/nsrdb-viewer"
    - Select GOES PSM v3 dropdown, and download "Multi Year PSM Direct Normal Irradiance" and "Multi Year PSM Global Horizontal Irradiance"
- Weather data from NOAA: "https://www.ncei.noaa.gov/pub/data/normals/1981-2010/" 
    - Our project used 1981-2010 30 year Climate Normals, but newer data has become available.
    - download "allstations.txt" from "https://www.ncei.noaa.gov/pub/data/normals/1981-2010/station-inventories/"
    - Download the following from "https://www.ncei.noaa.gov/pub/data/normals/1981-2010/products/precipitation/": 
		- ann-prcp-normal.txt
		- ann-snow-normal.txt
		- djf-prcp-normal.txt
		- djf-snow-normal.txt
		- jja-prcp-normal.txt
		- jja-snow-normal.txt
    - Download the following from "https://www.ncei.noaa.gov/pub/data/normals/1981-2010/products/precipitation/": 
		- ann-dutr-normal.txt
		- ann-tavg-normal.txt
		- ann-tmax-normal.txt
		- ann-tmin-normal.txt
		- djf-tavg-normal.txt
		- jja-tavg-normal.txt


The raw weather data is provided in a less intuitive format.
The following key to understanding the data format is taken from
https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt
"""
    A. FORMAT OF ANNUAL/SEASONAL FILES
       (ann-*.txt, djf-*.txt, mam-*.txt, jja-*.txt, son-*.txt)

       Each file contains the annual/seasonal values of one parameter at all
       qualifying stations. There is one record (line) per station.

       The variables in each record include the following:

       Variable  Columns  Type
       ----------------------------
       STNID       1- 11  Character
       VALUE      19- 23  Integer
       FLAG       24- 24  Character
       ----------------------------

       These variables have the following definitions:

       STNID   is the GHCN-Daily station identification code. See the lists in the
               station-inventories directory.
       VALUE1  is the annual/seasonal value.
       FLAG1   is the completeness flag for the annual/seasonal value. See Flags
               section below.

    E. FORMAT OF STATION INVENTORIES
       (*-inventory.txt, allstations.txt)

       Each file contains on station per line.

       The variables in each record include the following:
       ------------------------------
       Variable   Columns   Type
       ------------------------------
       ID            1-11   Character
       LATITUDE     13-20   Real
       LONGITUDE    22-30   Real
       ELEVATION    32-37   Real
       STATE        39-40   Character
       NAME         42-71   Character
       GSNFLAG      73-75   Character
       HCNFLAG      77-79   Character
       WMOID        81-85   Character
       METHOD*      87-99   Character
       ------------------------------

    UNITS:
           hundredths of inches for average monthly/seasonal/annual precipitation,
    month-to-date/year-to-date precipitation, and percentiles of precipitation.
    e.g., "1" is 0.01" and "1486" is 14.86"

        tenths of inches for average monthly/seasonal/annual snowfall,
    month-to-date/year-to-date snowfall, and percentiles of snowfall.
    e.g. "39" is 3.9"
"""
 
