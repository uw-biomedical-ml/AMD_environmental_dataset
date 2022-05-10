import csv
import numpy as np
from sklearn.neighbors import BallTree
import python_utils as pu

GHI_list = pu.make_list_from_tsv("processed_data/ghi_lonlat.tsv")
DNI_list = pu.make_list_from_tsv("processed_data/dni_lonlat.tsv")
zcta_list = pu.custom_read_zcta_tsv("processed_data/zcta_intpt.tsv")

zcta_ghi_list = pu.match_centroids(zcta_list,
                             GHI_list,
                             col_pos_dict = {'metric':[0],'lon':1,'lat':2})
with open("processed_data/zcta_ghi.tsv",'w') as fout:
    fout.write("ZCTA\tghi\n")
    for row in zcta_ghi_list:
        fout.write(f"{row[0]}\t{row[1]}\n")

zcta_list.insert(0,'replacement_header_filler')
zcta_dni_list = pu.match_centroids(zcta_list,
                             DNI_list,
                             col_pos_dict = {'metric':[0],'lon':1,'lat':2})
with open("processed_data/zcta_dni.tsv",'w') as fout:
    fout.write("ZCTA\tdni\n")
    for row in zcta_dni_list:
        fout.write(f"{row[0]}\t{row[1]}\n")
