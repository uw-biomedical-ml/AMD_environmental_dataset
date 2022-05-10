import csv
import copy
import os
import sys
sys.path.append("/Users/matthewhunt/Coding/Seattle_Research/IRIS_AMD_Environmental/Environmental_Data_Open_Source_Repo/code/")
import python_utils as pu

"""We formerly did the matching and merging separately, in different files, using R to merge a bunch of
tables that were formed by matching each measuremnet to nearest ZCTA center based on haversine dist w/
lat/lon pairs.

Now we'll do it all in one file and update the existing weather info matrix, zcta_master_info.tsv
The other difference is that we will treat each pollutant metric separately, always matching only to the
nearest non-nan value.
"""

load_dir ="processed_data"
save_dir = load_dir
### Inputs
#The file to update
weather_master_zcta_info = "zcta_master_info.tsv"
# The zcta file w/ lat lon for doing the matching.
zcta_latlon_file = "zcta_intpt.tsv"

wideform_pollutant_file = "no_duplicates_wideform_reduced_annual_conc_by_monitor_2017.csv"

### Outputs
updated_zcta_master_info_file = "zcta_master_with_pollution.tsv"

#again, gotta use this so we can keep leading zeros on zctas.
zcta_list = pu.custom_read_zcta_tsv(os.path.join(load_dir,zcta_latlon_file))
print(f"len of zcta_list is {len(zcta_list)}")
with open(os.path.join(load_dir,wideform_pollutant_file),'r') as fin:
    reader=csv.reader(fin,delimiter=',')
    pollutant_header = next(reader)
    phd = {el:i for i,el in enumerate(pollutant_header)}
    wideform_pollutant_list = [[row[0]]+[float(e) if e!='nan' else None for e in row[1:]] for row in reader]

# wideform_pollutant_list = pu.make_list_from_tsv(wideform_pollutant_file,nanchar='nan',delim=',')
pollutants_to_keep = ['Carbon monoxide','Sulfur dioxide','Nitrogen dioxide (NO2)','Ozone','PM2.5 - Local Conditions']



# zcta_header = zcta_list[0]
# zhd = {el:i for i,el in enumerate(zcta_header)}

#Get the master list going which will be our output
master_list_to_update = []
with open(os.path.join(load_dir,weather_master_zcta_info),'r') as master_in:
    nanchar = '`'
    reader=csv.reader(master_in,delimiter='\t')
    master_header = next(reader)
    master_hd = {el:i for i,el in enumerate(master_header)}
    for row in reader:
        master_list_to_update.append([row[0]]+[float(e) if e!=nanchar else None for e in row[1:]])
print(f'incoming master tsv file has {len(master_header)} columns and {len(master_list_to_update)} rows')

for pollutant in pollutants_to_keep:
    single_pollutant_list = [ [r[phd["Latitude"]],r[phd["Longitude"]],r[phd[pollutant]]] for r in
                             wideform_pollutant_list if r[phd[pollutant]] is not None]
    single_pollutant_list.insert(0,["Latitude",'Longitude',pollutant])# Teh next function pops the header

    zcta_pollutant_matched_list = pu.match_centroids(copy.deepcopy(zcta_list),
                                                     copy.deepcopy(single_pollutant_list),
                                                     {'lat':0,'lon':1,'metric':[2]})
    assert len(zcta_pollutant_matched_list[0]) == 2 # Just to make sure we're not matching mult metrics
    zcta_pollutant_matched_dict = {r[0]:r[1] for r in zcta_pollutant_matched_list}

    #Just using the full iteration each time bc it's more readable than a nested dict!
    master_header.append(pollutant)
    for row in master_list_to_update:
        zcta = row[master_hd['ZCTA5CE10']]
        try:
            row.append(zcta_pollutant_matched_dict[zcta])
        except:
            import pdb; pdb.set_trace()


print(f'writing out final file with {len(master_header)} columns and {len(master_list_to_update)} rows')
with open(os.path.join(save_dir,updated_zcta_master_info_file),'w') as fout:
    fout.write('\t'.join(master_header)+'\n')
    for row in master_list_to_update:
        fout.write('\t'.join([str(e) for e in row])+'\n')

#we want to write out to both places
with open(os.path.join("final_data",updated_zcta_master_info_file),'w') as fout:
    fout.write('\t'.join(master_header)+'\n')
    for row in master_list_to_update:
        fout.write('\t'.join([str(e) for e in row])+'\n')
