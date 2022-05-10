from collections import Counter
import numpy as np
import os
import csv
import pandas as pd

"""Core Idea: Each uid will come out representing a single parameter measurment with mean and lat/lon.
We'll use a dict at first to allow for proper prioritizing"""
"""
This file accomplishes two main things
1. It makes the filtered version of the large aqi file s.t. we retain only pollutants_of_interest,
2. makes the wideform version of this.
"""


raw_dirpath = "raw_data_sources/"
complete_env_file = "annual_conc_by_monitor_2017.csv"
save_dirpath = "processed_data"
savefile = "reduced_annual_conc_by_monitor_2017.csv"
wideform_file = "wideform_reduced_annual_conc_by_monitor_2017.csv"

final_cols = ["Unique_ID","POC","Latitude","Longitude","Parameter_Name","Sample_Duration","Pollutant_Standard",
              "Metric_Used","Units_of_Measure","Event_Type","Completeness_Indicator","Arithmetic_Mean"]

uid_info_dict = {} #Got to start with a dictionary because out to be efficient how we iterate
"""The structure of this is
    {uid:
        { pollutant :
            {all other final_cols info needed & a 'priority':Values in table}}}"""

prioritizing_cols = ["Sample Duration","Pollutant Standard","Metric Used"] #used to assign priority
# This structure works by putting the pollutant as key, and then putting priority ordering as value
pollutants_of_interest = {"Carbon monoxide":{"8-HR RUN AVG END HOUR#####CO 8-hour 1971#####8-Hour running average (end hour) of observed hourly values":1},
                          "Lead (TSP) LC":{"24 HOUR#####Lead 3-Month 2009#####Observed Values":1},
                          "Nitrogen dioxide (NO2)":{"1 HOUR#####NO2 1-hour 2010#####Daily Maximum 1-hour average":1},
                            "Ozone":{ "8-HR RUN AVG BEGIN HOUR#####Ozone 8-Hour 1997#####Daily maximum of 8 hour running average of observed hourly values":3,
                                    "8-HR RUN AVG BEGIN HOUR#####Ozone 8-Hour 2008#####Daily maximum of 8 hour running average of observed hourly values":2,
                                    "8-HR RUN AVG BEGIN HOUR#####Ozone 8-hour 2015#####Daily maximum of 8-hour running average":1},
                          "PM2.5 - Local Conditions": {"24-HR BLK AVG#####PM25 24-hour 1997#####Daily Mean":6,
                                                        "24-HR BLK AVG#####PM25 24-hour 2006#####Daily Mean":5,
                                                        "24-HR BLK AVG#####PM25 24-hour 2012#####Daily Mean":4,
                                                        "24-HR BLK AVG#####PM25 Annual 1997#####Quarterly Means of Daily Means":3,
                                                        "24-HR BLK AVG#####PM25 Annual 2006#####Quarterly Means of Daily Means":2,
                                                        "24-HR BLK AVG#####PM25 Annual 2012#####Quarterly Means of Daily Means":1},
                          "PM10 - LC": {"24 HOUR##########Observed Values":1},
                          "Sulfur dioxide":{"1 HOUR#####SO2 1-hour 2010#####Daily maximum 1-hour average":1}
                         }


i = 0
with open(os.path.join(raw_dirpath,complete_env_file)) as f:
    reader = csv.reader(f,delimiter=",")
    header = next(reader)
    hd = {el:i for i,el in enumerate(header)}
    for row in reader:
#         if row[hd["POC"]] != "1":
#             continue
        uid = "-".join(row[:4]) #no longer includes POC.
        if row[hd["Event Type"]] not in ["No Events","Events Included"]: # We include all data in the case of events present
            continue
        poi = row[hd["Parameter Name"]]
        if poi not in pollutants_of_interest:
            continue
        prioritizing_string = "#####".join([row[hd[col]] for col in prioritizing_cols])
        ####Needed behavior
        priority = pollutants_of_interest[poi].get(prioritizing_string,None)
        if priority is None: #Must have a recognized pattern. Might wanna change later.
            continue


#         if uid not in uid_info_dict:
        uid_info_dict.setdefault(uid,{}).setdefault(poi,{})# = {poi:{} for poi in pollutants_of_interest.keys()}
        last_priority = uid_info_dict[uid][poi].get("priority",None)
        completeness = row[hd["Completeness Indicator"]]
        last_completeness = uid_info_dict[uid][poi].get("Completeness_Indicator",None)

        POC = row[hd["POC"]]
        last_POC = uid_info_dict[uid][poi].get("POC",None)

        # Logic here: We select lowest #'ed priority string, but we place completeness indicator as a higher
        # indication to overwrite. We force overwrite if get better completeness, and disallow if worse
        # completeness. If neither, we fall back to priority overwriting. lastly, in the event of tied
        # priority, we choose lowest POC. I think I'm misunderstanding POC anyway, but this should not
        # exclude anything at least.
        overwrite = False
        if (last_completeness is None or last_completeness == "N") and completeness == 'Y':
            overwrite = True
        elif last_completeness == 'Y' and completeness == 'N':
            overwrite = False
        elif last_priority is None or priority < last_priority:
            overwrite = True
        elif last_priority == priority and int(POC)<int(last_POC):
            overwrite = True

        if overwrite:
            uid_info_dict[uid][poi] = {col:row[hd[col.replace('_',' ')]] for col in final_cols[1:]} #Note, this structure is indeed dumb. We have the pollutant also as a value of the key...
            uid_info_dict[uid][poi]["priority"] = priority

        i+=1
#         if i==1000:
#             break


# Now save the file reading off the dictionary
summaries = {"POC":Counter(),
            "Parameter_Name":Counter(),
            "Completeness_Indicator":Counter(),
            "priority":Counter(),
            }
with open(os.path.join(save_dirpath,savefile),"w") as fout:
    fout.write(f"{','.join(final_cols)},Selection_Priority\n")
    for i,(uid,sub_d) in enumerate(uid_info_dict.items()):
        for pollutant in sub_d.keys():
            try:
                info_list = [str(sub_d[pollutant][col]) for col in final_cols[1:]+["priority"]]
            except Exception as e:
                print(e)
                import pdb; pdb.set_trace()
            fout.write(f"{uid},{','.join(info_list)}\n")
            for k,c in summaries.items():
                c.update([str(sub_d[pollutant][k])])

for k,c in summaries.items():
    print(k)
    for thing,count in c.items():
        print(f"\t{thing}:{count}")


### Now we make the wideform file

pollutants = ["Carbon monoxide", "Sulfur dioxide", "Nitrogen dioxide (NO2)", "Ozone", "PM10 - LC", "PM2.5 - Local Conditions", "Lead (TSP) LC"]

columns_to_keep = ["Latitude","Longitude"]+pollutants
def make_wideform_list(longform_df_file):
    """Note I should make the pairplots file use the output of this"""
    """Takes in a longform df like our filtered excel file and outputs a wideform version where each unique
    code is paired w/ each pollutant or Nan"""
    with open(longform_df_file,'r') as f:
        reader = csv.reader(f,delimiter=',')
        header = next(reader)
        hd = {el:i for i,el in enumerate(header)}
        unique_station_dict = {}
        for row in reader:
            station_id = '-'.join(row[0].split('-')[:-1])
            if station_id not in unique_station_dict:
                unique_station_dict[station_id] = {"Latitude":row[hd["Latitude"]],
                                                   "Longitude":row[hd["Longitude"]]}
            param = row[hd['Parameter_Name']]
            if param in unique_station_dict[station_id]: #We've hopefully selected a single record at each location.
                import pdb; pdb.set_trace()
            unique_station_dict[station_id][param] = row[hd["Arithmetic_Mean"]]
    df_list = [["station_id"]+columns_to_keep]
    print(f"{len(unique_station_dict)} unique stations")
    for station_id,sub_d in unique_station_dict.items():
        ap_list = [sub_d.get(p,np.nan) for p in columns_to_keep]
        ap_list = [float(e) for e in ap_list]
        df_list.append([station_id]+ap_list)
    return df_list

wideform_list = make_wideform_list(os.path.join(save_dirpath,savefile))
with open(os.path.join(save_dirpath,wideform_file),'w') as fout:
    for row in wideform_list:
        str_row = [str(e) for e in row]
        fout.write(','.join(str_row)+'\n')
