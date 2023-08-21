"""
AF 8-2023

Getting bridge counts by year

    inputs: 
    ______

        "https://www.fhwa.dot.gov/bridge/nbi/{year}allstatesallrecsdel.zip"

            NBI records for YEAR
    
    outputs: 
    _______

        ~//data//processed//etl_2_bridge_condition_counts.csv


"""

##############
# SETTING UP #
##############

import pandas as pd
import numpy as np

processed = "..//data//processed//"

########################
# READING IN THE FILES #
########################

first_year = 2016
last_year = 2023

count_list = []

for year in range(first_year, last_year + 1): 

    year_url = f"https://www.fhwa.dot.gov/bridge/nbi/{year}allstatesallrecsdel.zip"

    df = pd.read_csv(year_url, compression="zip", encoding="ISO-8859-1")
    print(f"Number of records in {year}: {len(df)}")

    bridges = df[df.RECORD_TYPE_005A.astype(str) == "1"]
    print(f"Number of bridges in {year}: {len(bridges)}")

    if("CAT10" in bridges.columns):

        counts = bridges.CAT10.value_counts()
        counts.name = year
        counts.index.name = 'BRIDGE_CONDITION'
        
        count_list.append(counts)

        print(f"Done with {year}!\n")

    if("BRIDGE_CONDITION" in bridges.columns):

        counts = bridges.BRIDGE_CONDITION.value_counts()
        counts.name = year


        count_list.append(counts)

        print(f"Done with {year}!\n")

final = pd.concat(count_list, axis = 1)
    

####################
# WRITING OUT FILE #
####################

outfile_str = processed + "etl_2_bridge_condition_counts.csv"

final.to_csv(outfile_str)

print("WOOOHOOO")