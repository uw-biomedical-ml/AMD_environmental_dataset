import csv
import numpy as np
from sklearn.neighbors import BallTree
import python_utils as pu

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

DEM_zmeans_list = pu.make_list_from_tsv("processed_data/DEM_ul_lr_zmean.tsv")
DEM_centroids_list = make_DEM_centroids(DEM_zmeans_list)
zcta_list = pu.custom_read_zcta_tsv("processed_data/zcta_intpt.tsv")

_ = zcta_list.pop(0)
_ = DEM_centroids_list.pop(0)
zcta_array = np.deg2rad(np.array([row[1:] for row in zcta_list]))
DEM_array = np.deg2rad(np.array([row[:-1] for row in DEM_centroids_list]))
import sys
sys.setrecursionlimit(100000)
tree = BallTree(DEM_array,metric='haversine')
distances,indices = tree.query(zcta_array,k=1)
indices = list(np.ravel(indices))

zcta_zmean_list = [[row[0],DEM_centroids_list[indices[i]][-1]] for i,row in enumerate(zcta_list)]

with open("processed_data/zcta_zmean.tsv",'w') as fout:
    fout.write("ZCTA\tzmean\n")
    for row in zcta_zmean_list:
        fout.write(f"{row[0]}\t{row[1]}\n")
