#!/bin/bash
echo python code/05_latlon_weather_metric_mapping.py  
python code/05_latlon_weather_metric_mapping.py  &&
echo python code/06_make_zcta_to_zmean.py  
python code/06_make_zcta_to_zmean.py  &&
echo python code/07_make_zcta_ghi_zcta_dni.py  
python code/07_make_zcta_ghi_zcta_dni.py  &&
echo python code/08_make_zcta_weather_metrics_tsv.py 
python code/08_make_zcta_weather_metrics_tsv.py 
