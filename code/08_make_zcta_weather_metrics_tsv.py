import csv
import numpy as np
from sklearn.neighbors import BallTree
import python_utils as pu
weather_list = pu.make_list_from_tsv("processed_data/lonlat_weather_metrics.tsv")
zcta_list = pu.custom_read_zcta_tsv("processed_data/zcta_intpt.tsv")

weather_header = weather_list[0]
col_pos_dict = {'lon':0,
                'lat':1,}
metric_inds = list(range(len(weather_list[0])))
metric_inds.remove(col_pos_dict['lon'])
metric_inds.remove(col_pos_dict['lat'])
col_pos_dict['metric'] = metric_inds

zcta_weather_list = pu.match_centroids(zcta_list,weather_list,col_pos_dict)

with open("processed_data/zcta_weather.tsv",'w') as fout:
    header_str = "ZCTA\t"+'\t'.join(weather_header[2:])+"\n"
    fout.write(header_str)
    for row in zcta_weather_list:
        row = [0.0 if el == -7777 else el for el in row]
        row_str = "\t".join([str(el) for el in row])+"\n"
        fout.write(row_str)
