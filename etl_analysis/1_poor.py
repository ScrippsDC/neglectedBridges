"""
AF 8-2023

Database of all bridges in poor condition and other characteristics 

    inputs: 
    ______

        ~//data//infobridge//Poor_{first_year}_Poor_2022.txt

        ~//data//NBI//2023AllRecordsDelimitedAllStates.txt


    outputs: 
    _______

        ~//data//processed//etl_1_poor.csv


"""

##############
# SETTING UP #
##############

import pandas as pd
import numpy as np

infobridge = "../data/infobridge/"
processed = "../data/processed/"
nbi = "..//data//NBI//"

first_year = 2014
last_year = 2022

poor_str = infobridge + f"Poor_{first_year}_Poor_{last_year}.txt"
nbi_str = nbi + "2023AllRecordsDelimitedAllStates.txt"
FIPS_str = "https://www2.census.gov/geo/docs/reference/codes2020/national_state2020.txt"

########################
# READING IN THE FILES #
########################

poor = pd.read_csv(poor_str, quotechar= "'")
print(f"Prelim # of consistently poor bridges: {len(poor)}")
nbi = pd.read_csv(nbi_str)
print(f"Number of records in NBI: {len(nbi)}")

#############
# FILTERING #
#############

# only keep records describing bridges
nbi = nbi[nbi['RECORD_TYPE_005A'].astype(str)=='1']
print(f"Number of records describing bridges in NBI: {len(nbi)}")
nbi = nbi[nbi.BRIDGE_CONDITION =="P"]
print(f"Number of bridges rated poor in 2023: {len(nbi)}")

# Bridges poor or missing in intermediary years
for year in range(first_year, last_year+1): 
    poor = poor[(poor[str(year)] == "Poor") | poor[str(year)].isnull()]
    # print(f"{year}: {len(poor)} bridges")

all_poor = poor
print(f"Number of bridges that were poor (or missing) all years between {first_year} and {last_year}: {len(all_poor)}")

#############
# COMBINING #
#############

# add state fips code to nbi
fips = pd.read_csv(FIPS_str, delimiter ="|", usecols = ['STATEFP', 'STATE_NAME'])
nbi_fips = pd.merge(fips, nbi, left_on="STATEFP", right_on="STATE_CODE_001", how='right')

# create unique ID 
all_poor['ID'] = all_poor['1 - State Name'] + "_" + all_poor['8 - Structure Number'].str.strip().str.lstrip("0")
nbi_fips['ID'] = nbi_fips['STATE_NAME'].astype(str) + "_" + nbi_fips['STRUCTURE_NUMBER_008'].astype(str).str.strip().str.lstrip("0")

# pull 2023 NBI records for bridges in all_poor
final = nbi_fips[nbi_fips.ID.isin(all_poor.ID)]

print(f"Dimensions of final (including closed bridges): {final.shape}")

# only include open bridges 
final = final[final['OPEN_CLOSED_POSTED_041']!="K"]

####################
# WRITING OUT FILE #
####################

outfile_str = processed + "etl_1_poor.csv"
final.to_csv(outfile_str, index=False)

############
# ANALYSIS #
############

print(f"Dimensions of final (not including closed bridges): {final.shape}")

print(f"Number of unique states: {final['STATE_NAME'].nunique()}")

print(f"Total Ridership: {sum(final['ADT_029'])}")

print(f"Total cost of improvements: { sum(final['TOTAL_IMP_COST_096'].fillna(0))*1000}")


print("WOOOHOOO")