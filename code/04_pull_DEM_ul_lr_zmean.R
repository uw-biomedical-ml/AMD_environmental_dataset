library(sf)
library(ggplot2)

DEM_data=st_read('raw_data_sources/FESM_1.gpkg')
print(head(DEM_data))

ul_lr_zmean = st_drop_geometry(DEM_data[,c('lrlat','lrlon','ullat','ullon','zmean')])

write.table(x=ul_lr_zmean,file="processed_data/DEM_ul_lr_zmean.tsv",
            sep="\t", na='`',
            quote=F,row.names=F)
