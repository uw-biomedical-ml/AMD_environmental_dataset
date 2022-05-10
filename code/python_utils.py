import numpy as np
import csv
from sklearn.neighbors import BallTree


def make_list_from_tsv(tsv_in):
    tsv_list = []
    with open(tsv_in,'r') as fin:
        reader = csv.reader(fin,delimiter='\t')
        header = next(reader)
        tsv_list.append(header)
        for row in reader:
            to_append = [float(el) if el!='`' else None for el in row]
            tsv_list.append(to_append)
    #         = [[float(el) for el in row] for row in reader]
    return tsv_list

def custom_read_zcta_tsv(tsv_in):
    """so dumb but i need the zips to keep the leading zeros"""
    tsv_list = []
    with open(tsv_in,'r') as fin:
        reader = csv.reader(fin,delimiter='\t')
        header = next(reader)
        tsv_list.append(header)
        for row in reader:
            to_append = [str(row[0]),
                         float(row[1]) if row[1]!='`' else None,
                         float(row[2]) if row[2]!='`' else None]
            tsv_list.append(to_append)
    return tsv_list

def match_centroids(zcta_list,other_list,col_pos_dict):
    """selects the matching centroids to teh zcta INTPT given.
    input: zcta and other list, which have latlon info and some metric we wish to match with zcta
    col_pos_dict should be {'lat':#,'lon':#,'metri':list(#'s)}
    Returns -->zcta_and_metric list
    """
    cpd = col_pos_dict
    _ = zcta_list.pop(0)
    _ = other_list.pop(0)
    zcta_array = np.deg2rad(np.array([row[1:] for row in zcta_list]))
    other_array = np.deg2rad(np.array([[row[cpd['lon']],row[cpd['lat']]] for row in other_list]))
    import sys
    sys.setrecursionlimit(100000)
    tree = BallTree(other_array,metric='haversine')
    distances,indices = tree.query(zcta_array,k=1)
    indices = list(np.ravel(indices))
    zcta_metric_list = []
    for i, row in enumerate(zcta_list):
        zcta = [row[0]]
        metrics = [other_list[indices[i]][j] for j in cpd['metric']]
        zcta_metric_list.append(zcta+metrics) #concat these 2 lists
        # This structure allows flexible # metrics
#     zcta_metric_list = [[row[0],for i,row in enumerate(zcta_list)]
    return zcta_metric_list

def match_centroids_ghi(ghi_list,GHI_DNI_col_pos_dict,other_list,other_col_pos_dict,metric_name='Fill'):
    """does the same as above, but takes in a list of other lists and matches their closest centroids to teh
    ghi tsv. Also, we presever the lat and lon of the ghi bc we need those later.
    Note that because dni is the same coords as ghi, we can just make some kind of absolute match between
    them or just use balltree. Either way should be fine.
    Maybe lets to balltree and make sure it worked w/ assert
    """
    cpd = other_col_pos_dict
    gcpd = GHI_DNI_col_pos_dict
    original_header = ghi_list.pop(0)
    _ = other_list.pop(0)
    ghi_array = np.deg2rad(np.array([[row[gcpd['lon']],row[gcpd['lat']]] for row in ghi_list]))
    other_array = np.deg2rad(np.array([[row[cpd['lon']],row[cpd['lat']]] for row in other_list]))
    import sys
    sys.setrecursionlimit(100000)
    tree = BallTree(other_array,metric='haversine')
    distances,indices = tree.query(ghi_array,k=1)
    indices = list(np.ravel(indices))
    ghi_lon_lat_metric_list = []
    for i, row in enumerate(ghi_list):
#         ghi_lon_lat = [row[gcpd['metric']],row[gcpd['lon']],row[gcpd['lat']]]
        metrics = [other_list[indices[i]][j] for j in cpd['metric']]
        ghi_lon_lat_metric_list.append(row+metrics) #concat these 2 lists
        # This structure allows flexible # metrics
#     zcta_metric_list = [[row[0],for i,row in enumerate(zcta_list)]
    ghi_lon_lat_metric_list.insert(0,original_header+[n for n in metric_name])
    return ghi_lon_lat_metric_list


def write_tsv(master_list,filepath):
    with open(filepath,'w') as fout:
        for row in master_list:
            fout.write('\t'.join([str(el) for el in row])+'\n')

def read_tsv(filepath):
    with open(filepath,'r') as fout:
        reader = csv.reader(fout,delimiter='\t')
        list_out = [next(reader)]
        for row in reader:
            list_out.append([float(el) for el in row])
    return list_out
