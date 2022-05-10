library(sf)
library(ggplot2)

shapefile = read_sf("raw_data_sources/nsrdb_v3_0_1_1998_2016_ghi/nsrdb_v3_0_1_1998_2016_ghi.shp")
centroid_coords = st_coordinates(st_centroid(shapefile))
longitude = centroid_coords[,1]
latitude = centroid_coords[,2]
head(shapefile)
head(centroid_coords)

shapefile <- cbind(shapefile,longitude)
shapefile <- cbind(shapefile,latitude)
head(shapefile)

relevant_data = st_drop_geometry(shapefile[,c("ghi","longitude","latitude")])
write.table(x=relevant_data,file="processed_data/ghi_lonlat.tsv",
            sep="\t",na='`',
            quote=F,row.names=F)
