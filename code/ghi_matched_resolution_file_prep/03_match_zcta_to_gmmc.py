"""This file relies on the existance of ghi_matched_master_cleaned.tsv. Here we
match each ghi location with it's haversine-nearest neighbor. This is done so
we can predict at every ghi location using the mixed model approaches.

Might be more accurate to use the actual zcta each ghi loc lies w/in, and then
only do kdball matching for the ghi locs w/o a zcta they belong to.

output ghi_matched_master_cleaned_plus_zcta.tsv"""

import os
import csv
import numpy as np
from sklearn.neighbors import BallTree
import sys
sys.path.append("/Users/matthewhunt/Coding/Seattle_Research/IRIS_AMD_Environmental/Environmental_Data_Open_Source_Repo/code/")
import python_utils as pu

zcta_list = pu.custom_read_zcta_tsv("processed_data/zcta_intpt.tsv")

gmmc_file = "processed_data/ghi_matched_master_cleaned.tsv"


# gmmc_list = []
# with open(gmmc_file,'r') as fin:
#     reader = csv.reader(fin,delimiter='\t')
#     for row in reader:
#         gmmc_list.append(row)

gmmc_list = pu.make_list_from_tsv(gmmc_file)
gmmc_col_pos_dict = {'lon':1,'lat':2}
zcta_col_pos_dict = {'lon':1,'lat':2,'metric':[0]}

list_out = pu.match_centroids_ghi(gmmc_list,gmmc_col_pos_dict,zcta_list,zcta_col_pos_dict,metric_name=['zcta'])


pu.write_tsv(list_out,
             filepath = "final_data/ghi_matched_master_cleaned_plus_zcta.tsv")
