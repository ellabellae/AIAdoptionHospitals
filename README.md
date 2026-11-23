# AI Adoption and DRG Families Across U.S. Hospitals 

Ella Etchandy, Jessica Pham, Ella Fortenbery

## Sources and Instructions
HSA zipcodes and .geojson filescome from https://data.dartmouthatlas.org/supplemental/

Download `VSCode Map Preview` extension to visualize hotspot/coldspot map, located here: "HSA_Bdry__AK_HI_unmodified\hsa-geojson\HsaBdry_AK_HI_unmodified.geojson".

hsa_classifications.csv contains the classification of each HSA.

To update the coloring in the geojson map after changing AI classifications, run update_hsa_colors.py andreload the map in VSCode Map Preview.

## Data
- Load relevant hospitals from CMS: https://data.cms.gov/provider-summary-by-type-of-service/medicare-inpatient-hospitals/medicare-inpatient-hospitals-by-provider-and-service
- Run cells in get_data.ipynb to fetch and process hospital data, saved into hospital_data.csv.
- The same notebook also fetches the hospital-level "Medicare Inpatient Hospitals - by Provider" table (length of stay, HCC risk score, demographics, chronic conditions) for the same hospitals, saved into hospital_provider_data.csv: https://data.cms.gov/provider-summary-by-type-of-service/medicare-inpatient-hospitals/medicare-inpatient-hospitals-by-provider
- model.ipynb is setup to load data.

## LLM Usage
I used Codex to access and concatenate hospital data from multiple years into a single CSV file, only keeping hospitals whose zipcode maps to a significant AI usage cluster.

## Held-out prediction map

Run the held-out evaluation and **Export held-out predictions for mapping** cells
in `model.ipynb` to save `graphing_maps/predicted_results.csv` directly from the
evaluated predictions, without retraining. DRG probabilities within each hospital-year
are weighted by `Tot_Dschrgs` (discharges, a patient-volume proxy). Then run:

```powershell
python graphing_maps/prediction_results_map.py
python graphing_maps/plot_predicted.py
```

The first command colors `HSA_Bdry__AK_HI_unmodified/hsa-geojson/predicted_results.geojson`;
the second exports the paper figures to `graphing_maps/`. Use `--year 2023` on
the first command to select a year. Rerun the notebook export and both commands
when model predictions change. The original classification map is preserved.

Map colors: blue = true coldspot/called coldspot; dark purple = true coldspot/called
hotspot; purple = true hotspot/called coldspot; red = true hotspot/called hotspot.
Gray indicates no held-out predictions for that year. The default year is the
latest in the CSV. Within each HSA, hospital-year probabilities are averaged
with equal hospital weight and thresholded at 0.5; map properties include the
probability and number of test hospitals. Therefore, HSA color counts differ
from the hospital-year confusion matrix, which combines both years.

Map plotting scripts and figure outputs are in `graphing_maps/`. Run
`python graphing_maps/plot_predicted.py` or
`python graphing_maps/map_classification.py` from the project root.
Script paths are resolved relative to their files, so they also work from other directories.
