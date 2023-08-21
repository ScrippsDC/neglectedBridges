# Neglected Bridges

This repository contains data and code to reproduce the data findings in [Thousands of bridges left behind in race to rebuild infrastructure](https://scrippsnews.com/stories/thousands-of-bridges-left-behind-in-race-to-rebuild-infrastructure/), published on August 10, 2023.

Namely: 

>More than 14,000 bridges in all 50 states and Washington, D.C., have been ranked in poor condition for at least a decade. Combined, they carry over 46 million passengers every day. While a bridge in "poor" condition doesn't mean it will collapse, it may require weight limits for trucks and more frequent inspections. Bridges in poor condition are at greater risk of closure for safety concerns. Repairing all of the poor bridges identified in the Scripps News analysis would cost at least $97 billion.

## Data

The [National Bridge Inventory](https://www.fhwa.dot.gov/bridge/mtguide.cfm) was the main data source of this piece, updated annually. Data on bridge conditions from 2014-2022 is from the [InfoBridge portal](https://infobridge.fhwa.dot.gov/Data/Dashboard).

Under the "Bridge Condition Transition History" tab, we filtered for bridges that had a poor rating in 2014 and a poor rating in 2022. (During ETL, we filtered for bridges that were (1) poorly rated or (2) not rated from 2015-2021.) This file is saved at `data/infobridge/Poor_2014_Poor_2022.txt`.

The 2023 NBI data was released on June 27th, 2023 but not yet available in InfoBridge. As a result, we downloaded the 2023 data directly from the [NBI site](https://www.fhwa.dot.gov/bridge/nbi/ascii2023.cfm), specifically the version under "Download all records. Includes non-highway and routes under bridges zip file (57 mb).)" This file is saved at `data/NBI/2023AllRecordsDelimitedAllStates.txt` but is not included in this repository because it is larger than GitHub's 100MB file limit.

Documentation for the NBI can be found [here](https://www.fhwa.dot.gov/bridge/mtguide.pdf).

## ETL and analysis

All the etl and analysis for this piece is in the file `etl_analysis/1_poor.py`, which was run in the terminal. 

### ETL summary:

* Start with `Poor_2014_Poor_2022.txt`: 20,008 rows
* Filter for bridges that were also poor for all years (or had gaps in their inspection record) from 2015-2021: 18,354 rows
* Left joined with `2023AllRecordsDelimitedAllStates.txt` on the unique identifier (state and bridge ID), filtering for bridges that were poor in 2023: 16,220 rows       
    * When creating the unique identifier, leading and trailing whitespace, as well as leading 0s, were removed from the bridge ID.
* Filtered only for bridges that were open in 2023 (aka where “OPEN_CLOSED_POSTED_041” was not “K”): 14,570 rows   
* Output saved at: `data/processed/etl_1_poor.csv`

### Analysis:

* Count the number of bridges: 14,570
* Count the number of states: 50 states + DC + Puerto Rico (52 total)
* Sum the ridership ('ADT_029'): 46,587,345
* Sum the costs of improvement ('TOTAL_IMP_COST_096', replacing NaNs): $97,366,070,000

## Graphics 

For the interactive map in the digital piece, we used the coordinates from the 2022 data (`data/infobridge/NBI_2022_Poor.txt`). For the following cases, the 2022 coordinates were clearly outside of the United States, and we manually replaced the coordinates with data from previous years:
* https://infobridge.fhwa.dot.gov/Data/BridgeDetail/23743484
* https://infobridge.fhwa.dot.gov/Data/BridgeDetail/23703612
* https://infobridge.fhwa.dot.gov/Data/BridgeDetail/23704051
* https://infobridge.fhwa.dot.gov/Data/BridgeDetail/23704052
* https://infobridge.fhwa.dot.gov/Data/BridgeDetail/23704340
* https://infobridge.fhwa.dot.gov/Data/BridgeDetail/23700180
* https://infobridge.fhwa.dot.gov/Data/BridgeDetail/23703351

The dataset to create the Flourish graphic is at: `data/manual/flourish_map.csv`

## Other data elements

In the video piece, there is a map of counties that received funding from the Bipartisan Infrastructure Law. The list of counties was taken from the [Bipartisan Infrastructure Law (BIL) Maps Dashboard](https://d2d.gsa.gov/report/bipartisan-infrastructure-law-bil-maps-dashboard), filtering for projects containing the word "bridge". To get the coordinates, the counties were mapped in Tableau and their coordinates were exported as a csv and deduplicated. The list of coordinates can be found at `data/manual/BIL_bridge_project_coordinates_dedupe_reformat.csv`.