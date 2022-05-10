def append_station_map(station_map,input_txt):
    """appends the metric from input_txt to the station_map dictionary.
    This function will be executed 1x per metric type we have, and the header must be named in corresponding
    order.
    """
    with open(input_txt,'r') as fin:
        for r in fin:
            station_id = r[0:11]
            value = r[18:23].strip(' ')
            station_map[station_id].append(value)

directory = 'raw_data_sources/weather_data/'

# Map station_id-->lat_lon
station_map = {}
with open(directory+'allstations.txt','r') as fin:
    for r in fin:
        station_id = r[0:11]
        lat = r[12:20]
        lon = r[21:30]
        station_map[station_id]=[lon,lat]

files_to_process = [
                    'ann-tavg-normal.txt', 'ann-tmax-normal.txt', 'ann-tmin-normal.txt',
                    'ann-dutr-normal.txt', 'djf-tavg-normal.txt', 'jja-tavg-normal.txt',
                    'ann-prcp-normal.txt','ann-snow-normal.txt','djf-prcp-normal.txt',
                    'djf-snow-normal.txt', 'jja-prcp-normal.txt', 'jja-snow-normal.txt'
                   ]
for fname in files_to_process:
    input_txt = directory+fname
    append_station_map(station_map,input_txt)

files_header = [s[0:8].replace('-','_') for s in files_to_process]
header = ['longitude','latitude'] + files_header
valid_length = len(header)
header_str = '\t'.join(header)+'\n'
print(f'header is {header_str}')
accepted_rows = 0
with open('processed_data/lonlat_weather_metrics.tsv','w') as fout:
    fout.write(header_str)
    for stnid,metric_row in station_map.items():
        if len(metric_row) == valid_length:
            row_str = '\t'.join(metric_row)+'\n'
            fout.write(row_str)
            accepted_rows += 1

"""see the word document for explanation. The non-accepted rows I think are not an issue"""

print(f"total stations: {len(station_map)}")
print(f"accepted stations: {accepted_rows}")
