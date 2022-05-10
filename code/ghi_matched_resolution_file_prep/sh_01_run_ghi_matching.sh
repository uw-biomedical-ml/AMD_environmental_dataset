#!/bin/bash

d="code/ghi_matched_resolution_file_prep"
echo $d/01_match_centroids_ghi.py 
python $d/01_match_centroids_ghi.py &&
echo $d/02_clean_ghi_matched_master.py 
python $d/02_clean_ghi_matched_master.py &&
echo $d/03_match_zcta_to_gmmc.py
python $d/03_match_zcta_to_gmmc.py

