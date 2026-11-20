"""Color HSA boundaries using the held-out predictions exported by model.ipynb.

Run: python graphing_maps/prediction_results_map.py [--year 2023]
The CSV retains hospital-year results; the map pools test hospitals within an
HSA for the selected year using their mean probability and a 0.5 threshold.
"""

import argparse
import json
from pathlib import Path

import pandas as pd

MAP_DIR = Path(__file__).resolve().parent
ROOT = MAP_DIR.parent
GEOJSON = ROOT / "HSA_Bdry__AK_HI_unmodified/hsa-geojson/HsaBdry_AK_HI_unmodified.geojson"
CSV = MAP_DIR / "predicted_results.csv"
OUTPUT = GEOJSON.with_name("predicted_results.geojson")
COLORS = {
    (0, 0): ("true coldspot, called coldspot", "#0080ff"),
    (0, 1): ("true coldspot, called hotspot", "#4602FF"),
    (1, 0): ("true hotspot, called coldspot", "#B863F1"),
    (1, 1): ("true hotspot, called hotspot", "#d73027"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, help="Map year (default: latest in CSV)")
    args = parser.parse_args()
    if not CSV.exists():
        raise FileNotFoundError(
            "Run the held-out evaluation and prediction export cells in model.ipynb first: " + str(CSV))
    results = pd.read_csv(CSV, dtype={"Rndrng_Prvdr_CCN": "string"})
    if results.duplicated(["Rndrng_Prvdr_CCN", "data_year"]).any():
        raise ValueError("Duplicate hospital-year predictions in CSV.")
    if not results.ai_class.isin([0, 1]).all() or not results.p_hotspot.between(0, 1).all():
        raise ValueError("CSV requires binary ai_class and probabilities between 0 and 1.")
    year = args.year if args.year is not None else int(results.data_year.max())
    selected = results.loc[results.data_year == year]
    if selected.empty:
        raise ValueError(f"No predictions for {year}.")
    if selected.hsa_id.isna().any() or selected.groupby("hsa_id").ai_class.nunique().gt(1).any():
        raise ValueError("Missing HSA IDs or conflicting true labels within an HSA.")
    pooled = selected.groupby("hsa_id").agg(
        ai_class=("ai_class", "first"), p_hotspot=("p_hotspot", "mean"),
        n_hospitals=("Rndrng_Prvdr_CCN", "nunique")
    )
    data = json.loads(GEOJSON.read_text(encoding="utf-8"))
    ids = {int(f["properties"]["HSA93"]) for f in data["features"]}
    if not set(pooled.index).issubset(ids):
        raise ValueError("Prediction HSA IDs are missing from the GeoJSON.")
    for feature in data["features"]:
        props = feature["properties"]
        hsa = int(props["HSA93"])
        props.update(prediction_year=year, prediction_outcome="no held-out predictions",
                     prediction_probability=None, prediction_true_class=None,
                     prediction_class=None, prediction_hospitals=0,
                     fill="#d9d9d9", **{"fill-opacity": 0.15})
        if hsa in pooled.index:
            row = pooled.loc[hsa]
            predicted = int(row.p_hotspot >= 0.5)
            outcome, color = COLORS[(int(row.ai_class), predicted)]
            props.update(prediction_outcome=outcome,
                         prediction_probability=float(row.p_hotspot),
                         prediction_true_class=int(row.ai_class), prediction_class=predicted,
                         prediction_hospitals=int(row.n_hospitals), fill=color,
                         **{"fill-opacity": 0.7})
    data["prediction_legend"] = {label: color for label, color in COLORS.values()}
    data["prediction_year"] = year
    OUTPUT.write_text(json.dumps(data, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Mapped {len(pooled)} HSAs for {year}: {OUTPUT}")
    for label, color in COLORS.values():
        print(f"  {color} {label}")


if __name__ == "__main__":
    main()
