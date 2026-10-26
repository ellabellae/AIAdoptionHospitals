# AI Adoption and DRG Families Across U.S. Hospitals 

Ella Etchandy, Jessica Pham, Ella Fortenbery

## Sources and Instructions
HSA zipcodes and .geojson filescome from https://data.dartmouthatlas.org/supplemental/

Download `VSCode Map Preview` extension to visualize hotspot/coldspot map, located here: "HSA_Bdry__AK_HI_unmodified\hsa-geojson\HsaBdry_AK_HI_unmodified.geojson".

hsa_classifications.csv contains the classification of each HSA.

To update the coloring in the geojson map after changing AI classifications, run update_hsa_colors.png andreload the map in VSCode Map Preview.

## Data
- Load relevant hospitals from CMS: https://data.cms.gov/provider-summary-by-type-of-service/medicare-inpatient-hospitals/medicare-inpatient-hospitals-by-provider-and-service
- Run cells in get_data.ipynb to fetch and process hospital data, saved into hospital_data.csv.
- model.ipynb is setup to load data.

## LLM Usage
I used Codex to access and concatenate hospital data from multiple years into a single CSV file, only keeping hospitals whose zipcode maps to a significant AI usage cluster.