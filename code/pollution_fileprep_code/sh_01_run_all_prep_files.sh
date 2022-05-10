#!/bin/bash

d="code/pollution_fileprep_code"                                                                                                                                                
echo $d/01_filter_big_file.py 
python $d/01_filter_big_file.py &&
echo $d/02_filter_duplicates.py 
python $d/02_filter_duplicates.py &&
echo $d/03_update_zcta_master_info.py 
python $d/03_update_zcta_master_info.py 
