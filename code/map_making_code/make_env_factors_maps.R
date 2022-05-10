library(ggplot2)
library(ggvoronoi)
library(gridExtra)
library(scales)

new_and_drop_cols <- function(master_matrix){
    master_matrix$other_prcp = master_matrix$ann_prcp - master_matrix$djf_prcp
    master_matrix$other_snow = master_matrix$ann_snow - master_matrix$djf_snow
    master_matrix$postal_code = master_matrix$zcta
    drop_names = names(master_matrix) %in% c("zcta")
    master_matrix = master_matrix[!drop_names]

    print('dim and head of master matrix')
    print(dim(master_matrix))
    print(head(master_matrix))

    print('dropping columns')
    mm_lon_lat = master_matrix[c('longitude','latitude'),]
    drop_names = names(master_matrix) %in% c("wet_inj_AMD", "INTPTLON10",'wet_AMD', 'wet_inj_AMD','ann_prcp','ann_snow', 'jja_prcp', 'jja_snow')
    master_matrix = master_matrix[!drop_names]
    return(master_matrix)
}

scale_cols <- function(master_matrix){
    print('scaling the numerical columns')
    master_matrix[c('ann_tavg', 'ann_tmax', 'ann_tmin', 'ann_dutr', 'djf_tavg', 'jja_tavg')] = master_matrix[c('ann_tavg', 'ann_tmax', 'ann_tmin', 'ann_dutr', 'djf_tavg', 'jja_tavg')]/10
    master_matrix[c('other_prcp', 'djf_prcp')] = master_matrix[c('other_prcp', 'djf_prcp')]/100
    master_matrix[c('other_snow', 'djf_snow')] = master_matrix[c('other_snow', 'djf_snow')]/10
    master_matrix[c('zmean')] = master_matrix[c('zmean')]/1000 #Make in kilometers
    print(head(master_matrix))
    return(master_matrix)
}

####### Prep our high-res data frame ###########

env_data_dir = "processed_data/"
master_matrix_file = paste(c(env_data_dir,'ghi_matched_master_cleaned_plus_zcta.tsv'),collapse=(''))
master_matrix = read.table(file=master_matrix_file,
        colClasses=c("numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric","numeric","numeric","numeric","numeric","numeric","character"),
                header=T, sep='\t',
                na.strings=c('None','`'),
                stringsAsFactors = T)

master_matrix <- new_and_drop_cols(master_matrix)
master_matrix = master_matrix[complete.cases(master_matrix),]
master_matrix <- scale_cols(master_matrix)

### Write out and reload. These used to be in two separate files. Should refactor ###
save_file = paste0("processed_data/","prepped_mm.tsv")
write.table(x=master_matrix,file=save_file,
            sep="\t", na='`',
            quote=F,row.names=F)


print("You first need to run prep_mm.R, which does preparation using the other conda env")
# Yep, it's dumb to plot these at ghi resolution, but I just want to code
# quickly.


save_dir = "figures/"

mm_file = paste0("processed_data/","prepped_mm.tsv") #gotta use prepped b of the stupid conda env issues w/ r versions
master_matrix = read.table(file=mm_file,
                colClasses=c(rep("numeric",21),"character"),
                header=T, sep='\t',
                na.strings=c('None','`'),
                stringsAsFactors = T)

resolution = 1000000
if (resolution<1000000){
        master_matrix = master_matrix[1:resolution,]
}
transform='log10'

plot_list = list()
num_cols = 3
num_plots = 18
num_rows = ceiling(num_plots/num_cols)

states = map_data('state')
mapAR = (max(states$long)-min(states$long))/(max(states$lat)-min(states$lat))
master_matrix = master_matrix[master_matrix$latitude > min(states$lat) & master_matrix$latitude < max(states$lat), ]
master_matrix = master_matrix[master_matrix$longitude > min(states$long) & master_matrix$longitude < max(states$long), ]
# master_matrix = master_matrix[master_matrix$latitude > 25 & master_matrix$latitude < 50,]
# master_matrix = master_matrix[master_matrix$longitude >-130 & master_matrix$longitude < -60,]
#AR approach should work given we use coord_quickmap or even coord_fixed? IDK actually. Maybe only for coord fixed.
units_per_row = 5
u = "in"
margin = 0.25
# names_to_iter = names(master_matrix)[!names(master_matrix) %in% c('postal_code',"INTPTLAT10","latitude","longitude")]
# browser()
names_to_iter = c("ghi","dni","zmean","ann_tavg","ann_tmax","ann_tmin","ann_dutr","djf_tavg","jja_tavg","djf_prcp","djf_snow","other_prcp","other_snow","Carbon.monoxide","Sulfur.dioxide","Nitrogen.dioxide..NO2.","Ozone","PM2.5...Local.Conditions")

for (i in seq_along(names_to_iter)) {
    print(i)
    env_factor = names_to_iter[[i]]
    midvalue = mean(master_matrix[[env_factor]])
    minvalue = min(master_matrix[[env_factor]])
    maxvalue = max(master_matrix[[env_factor]])


#     title = paste(c(NAME_CONV_LIST[[env_factor]],' At resolution: ',resolution),collapse='')
    title = NAME_CONV_LIST[[env_factor]]
    print(env_factor)
    print(paste0("Processing: ",title))
    print(paste0("Has min,mid,max values of of: ",",",minvalue,",",midvalue,",",maxvalue))

  plot_list[[i]] <- ggplot(data = master_matrix,aes(x=longitude,y=latitude)) +
        geom_voronoi(aes(fill=as.numeric(.data[[env_factor]]),color=as.numeric(.data[[env_factor]])),size=0.001,outline=states)+
    #    coord_fixed() +
        coord_quickmap() +
#         scale_color_viridis_c(trans=transform)+
        guides(fill = guide_colorbar(barheight = unit(units_per_row-2*margin-0.25,u))) +
        guides(color = guide_colorbar(barheight = unit(units_per_row-2*margin-0.25,u))) +
#         scale_fill_gradient2(midpoint=midvalue,low='blue',high='red',mid="white") +
#         scale_color_gradient2(midpoint=midvalue,low='blue',high='red',mid = "white") +
        scale_fill_gradientn(colours = c("blue","white","red"),
                               values = rescale(c(minvalue,midvalue,maxvalue)),
                                guide = "colorbar", limits = c(minvalue,maxvalue)) +
        scale_color_gradientn(colours = c("blue","white","red"),
                               values = rescale(c(minvalue,midvalue,maxvalue)),
                                guide = "colorbar", limits = c(minvalue,maxvalue)) +
    #add the outline
#         geom_polygon(data=states,aes(x=long,y=lat),color='gray',group=states$group,size=0.01,fill=NA)+
        ggtitle(title) +
        theme(
          plot.title = element_text(size=20,hjust=0.5),
          axis.ticks =  element_blank(),
          axis.text = element_blank(),
          axis.title = element_blank(),
          legend.title = element_blank(),
          legend.text = element_text(size=15),
          plot.margin = unit(c(margin,margin,margin,margin),u)
          )
}
p <- grid.arrange(grobs=plot_list,ncol=num_cols)

total_height = num_rows*units_per_row
total_width = num_cols*units_per_row*mapAR
print(paste0("total height and width = ",total_height,",",total_width))
ggsave(paste0(save_dir,"all_env_factors_subplots_",resolution,".png"),height=total_height,width=total_width,units=u,p,dpi=300)
