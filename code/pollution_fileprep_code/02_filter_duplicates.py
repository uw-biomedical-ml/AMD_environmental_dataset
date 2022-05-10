import os
import csv
"""Here we have to remove the lat-lon duplicates from the wideform_file in order to perform our plotting (there are
only like 4 duplicates total, and they should occur where there is > 1 station at single location). What We
will do is take all possible non-NAN values, and for values that both are not an a.m., we will take the one
with the lower site number"""

wideform_file = "wideform_reduced_annual_conc_by_monitor_2017.csv"
load_dirpath = "processed_data"
save_dirpath = load_dirpath
file_out = "no_duplicates_wideform_reduced_annual_conc_by_monitor_2017.csv"

with open(os.path.join(load_dirpath,wideform_file),'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    hd = {el:i for i,el in enumerate(header)}
    xy_coords = {}
    duplicates = {}
    for row in reader:
        xy = (row[hd['Latitude']],row[hd["Longitude"]])
        if xy in xy_coords:
            if xy not in duplicates:
                duplicates[xy] = []
            duplicates[xy].append(row)
            continue
        xy_coords[xy] = row

print(f"# of duplicates is {len(duplicates)}")

for k,v in duplicates.items():
    print('original')
    print(xy_coords[k])
    print('duplicate')
    print(v)

print("now take the superset of valid values from duplicate locations")


for xy,row in duplicates.items():
    assert len(row)==1 #if there are multiple duplicates this'll tell us.
    row = row[0]
    orig_row = xy_coords[xy]
    duplicate_station_num = int(row[0].split('-')[-1])
    orig_station_num = int(orig_row[0].split('-')[-1])
    priority = 0 if orig_station_num < duplicate_station_num else 1

    new_row = []
    for i in range(len(row)):
        pair = [orig_row[i],row[i]]
#         print(pair)
        if pair[0]=="nan":
            new_row.append(pair[1])
        elif pair[1]=="nan":
            new_row.append(pair[0])
        else:
            new_row.append(pair[priority]) # if neither nan, take the prioritized
    xy_coords[xy] = new_row
    print(new_row)




with open(os.path.join(save_dirpath,file_out),'w') as fout:
    fout.write(','.join(header) + '\n')
    for row in xy_coords.values():
        fout.write(','.join(row)+'\n')
