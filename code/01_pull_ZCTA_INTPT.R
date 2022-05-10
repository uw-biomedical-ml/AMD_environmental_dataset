library(rgdal)
library(sf)
library(ggplot2)
library(tigris)
library(ggplot2)
options(tigris_use_cache=T)
zip_df <- zctas()
zcta_intpt = st_drop_geometry(zip_df[,c('ZCTA5CE10','INTPTLON10','INTPTLAT10')])

write.table(x=zcta_intpt,file="processed_data/zcta_intpt.tsv",
        sep="\t",na='`',
        quote=F,row.names=F)
