library(rgdal)
library(sf)
library(ggplot2)
library(tigris)
library(plyr)
options(tigris_use_cache=T)

get_col_names = function(table_file){
    table = read.table(file=table_file,
           header=T, sep='\t',
           na.strings='`',
           stringsAsFactors = F)
    col_names = colnames(table)[-1]
    print('column_names = ')
    print(col_names)
    return(col_names)
}


merge_tables = function(other_table_file,zcta_master){
    other_table = read.table(file=other_table_file,
           colClasses = c(
                          'character',
                          rep('numeric',count.fields(textConnection(readLines(other_table_file,n=1)),sep='\t')-1)
                          ),
           header=T, sep='\t',
           na.strings='`',
           stringsAsFactors = F)

    other_table <- rename(other_table,c("ZCTA"="ZCTA5CE10"))
    head(other_table)
    zcta_plus_other = merge(zcta_master,other_table,by="ZCTA5CE10",all.x=T)
    print(head(zcta_plus_other))

    return(zcta_plus_other)
}


zcta_master <- zctas()
head(zcta_master)

files_to_process = c("processed_data/zcta_zmean.tsv","processed_data/zcta_ghi.tsv","processed_data/zcta_dni.tsv","processed_data/zcta_weather.tsv")
column_list = c()
for (file in files_to_process) {
    zcta_master = merge_tables(file,zcta_master)
    column_list = c(column_list,get_col_names(file))
}


data_out = st_drop_geometry(zcta_master[,c('ZCTA5CE10','INTPTLON10','INTPTLAT10',column_list)])
print("The head of the data out is!")
print(head(data_out))
write.table(x=data_out,file="processed_data/zcta_master_info.tsv",
        sep="\t",na='`',
        quote=F,row.names=F)

# print("making dni by zip")
# ggplot(data=zcta_master)+
#   geom_sf(data=zcta_master,aes(fill=dni),size=0.01)
# ggsave("processed_data/dni_by_zip.pdf")
