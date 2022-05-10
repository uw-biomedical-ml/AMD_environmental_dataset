import os
import csv
import numpy as np
from sklearn.neighbors import BallTree
import sys
sys.path.append("/Users/matthewhunt/Coding/Seattle_Research/IRIS_AMD_Environmental/Environmental_Data_Open_Source_Repo/code/")
import python_utils as pu

"""Parameters"""
center_data = False
scale_weather = False
save_file = 'processed_data/ghi_matched_master.tsv'

def make_DEM_centroids(DEM_list):
    DEM_centroids_list = []
    header = DEM_list.pop(0)
    hd = {col:i for i,col in enumerate(header)}
    new_header = ['longitude','latitude','zmean']
    DEM_centroids_list.append(new_header)
    for row in DEM_list:
        longitude = (float(row[hd['ullon']])+float(row[hd['lrlon']]))/2
        latitude = (float(row[hd['ullat']])+float(row[hd['lrlat']]))/2
        DEM_centroids_list.append([longitude,latitude,row[hd['zmean']]])
    return DEM_centroids_list

def pull_pollution_lists(f):
    """Pulls the non-NAN values out of our cleaned nonduplicated pollution tsv
    and puts into separae simpler lists, each in a dictionary"""
    pollutants_of_interest = ["Carbon monoxide","Sulfur dioxide","Nitrogen dioxide (NO2)","Ozone","PM2.5 - Local Conditions"]
    pollution_dict_of_lists = {p:[["Longitude","Latitude",p]] for p in pollutants_of_interest}

    with open(f,'r') as fin:
        reader = csv.reader(fin,delimiter=',')
        header = next(reader)
        hd = {el:i for i,el in enumerate(header)}
        for row in reader:
            for p in pollutants_of_interest:
                if row[hd[p]] != 'nan':
                    to_append = [float(row[hd['Longitude']]),
                                 float(row[hd['Latitude']]),
                                 float(row[hd[p]])]
                    pollution_dict_of_lists[p].append(to_append)
    print("\nSummary of pollution_dict_of_lists")
    for k,v in pollution_dict_of_lists.items():
        print(f"\t{k}: {len(v)} items, including header")
    return pollution_dict_of_lists


GHI_list = pu.make_list_from_tsv("processed_data/ghi_lonlat.tsv")
DNI_list = pu.make_list_from_tsv("processed_data/dni_lonlat.tsv")
GHI_DNI_col_pos_dict = {'metric':[0],'lon':1,'lat':2}

## Setting up zmean
DEM_zmeans_list = pu.make_list_from_tsv("processed_data/DEM_ul_lr_zmean.tsv")
DEM_centroids_list = make_DEM_centroids(DEM_zmeans_list)
print(f"zmeans prior to zeroing: {DEM_centroids_list[:3]}")
if center_data:
    DEM_centroids_list = zero_mean(DEM_centroids_list,cols_to_exclude=['longitude','latitude'])
    print(f"zmeans after centering: {DEM_centroids_list[:3]}")
DEM_col_pos_dict = {'metric':[2],'lon':0,'lat':1}

## Setting up weather

weather_list = pu.make_list_from_tsv("processed_data/lonlat_weather_metrics.tsv")
# weather_list = transform_weather_list(weather_list)
weather_header = weather_list[0]
weather_col_pos_dict = {'lon':0,
                'lat':1,}
metric_inds = list(range(len(weather_header)))
metric_inds.remove(weather_col_pos_dict['lon'])
metric_inds.remove(weather_col_pos_dict['lat'])
weather_col_pos_dict['metric'] = metric_inds

## Setting up pollution
"""More challenging because of the Nan in our table here. We instead pull
non-nan simple lists from it and put in a dictionary"""
pollution_dict_of_lists = pull_pollution_lists("processed_data/no_duplicates_wideform_reduced_annual_conc_by_monitor_2017.csv")
# weather_list = transform_weather_list(weather_list)
pollution_col_pos_dict = {'lon':0,
                'lat':1,}
pollution_col_pos_dict['metric'] = [2] # we have these mini lists


master_list = GHI_list

for i,row in enumerate(master_list):
    row.append(DNI_list[i][GHI_DNI_col_pos_dict['metric'][0]])
header = master_list.pop(0)
hd = {el:i for i,el in enumerate(header)}
for i,row in enumerate(master_list):
    lat_copy = row[hd['latitude']]
    row.append(lat_copy)
header.append('INTPTLAT10')
master_list.insert(0,header)
print(f"top of master is now {master_list[:3]}")

### ELEVATION

f_str = "processed_data/ghi_dni_zmean_master.tsv"
overwrite = True
if os.path.exists(f_str) and overwrite == False:
    print(f'loading {f_str}')
    master_list = pu.read_tsv(f_str)
else:
    print(f'making new {f_str}')
#     DEM_centroids_list = DEM_centroids_list[:100]
    master_list = pu.match_centroids_ghi(master_list,
                                      GHI_DNI_col_pos_dict,
                                      DEM_centroids_list,
                                      DEM_col_pos_dict,
                                     metric_name=['zmean'])
    pu.write_tsv(master_list,f_str)

### WEATHER
f_str = "processed_data/ghi_dni_zmean_weather_master.tsv"
overwrite = True
if os.path.exists(f_str) and overwrite ==False:
    master_list = pu.read_tsv(f_str)
else:
    whd = {el:i for i,el in enumerate(weather_header)} #don't think this is used
    metric_name_list = [weather_header[m] for m in metric_inds]

#     weather_list = weather_list[:100]
    master_list = pu.match_centroids_ghi(master_list,GHI_DNI_col_pos_dict,weather_list,weather_col_pos_dict,metric_name=metric_name_list)
    pu.write_tsv(master_list,f_str)



### POLLUTION
"""This one is more challenging because we don't have a simple TSV format, but
rather there are a lot of NAN, and thus I actually need to make a Dictionary of
lists"""
f_str = "processed_data/ghi_dni_zmean_weather_pollution_master.tsv"
overwrite = True
if os.path.exists(f_str) and overwrite == False:
    master_list = pu.read_tsv(f_str)
else:
    for pollutant, lon_lat_metric in pollution_dict_of_lists.items():
        # lon_lat_metric is the list for the specific pollutant. You pass in
        # with the header, and it's like [longitude,latitude,pollutant_value]
        master_list = pu.match_centroids_ghi(master_list,
                                             GHI_DNI_col_pos_dict,
                                             lon_lat_metric,
                                             pollution_col_pos_dict,
                                             metric_name=[pollutant])
    import pdb; pdb.set_trace()
    pu.write_tsv(master_list,f_str)




pu.write_tsv(master_list,save_file)
