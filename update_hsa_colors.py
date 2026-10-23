"""Apply CSV classifications and preview colors to the HSA GeoJSON."""

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GEOJSON = ROOT / "HSA_Bdry__AK_HI_unmodified/hsa-geojson/HsaBdry_AK_HI_unmodified.geojson"


def main():
    with (ROOT / "hsa_classifications.csv").open(newline="", encoding="utf-8-sig") as handle:
        classifications = {}
        for row in csv.DictReader(handle):
            hsa = int(row["HSA93"])
            value = int(row["classification"])
            if hsa in classifications or value not in (-1, 0, 1):
                raise ValueError(f"Duplicate HSA or invalid classification: {row}")
            classifications[hsa] = value

    data = json.loads(GEOJSON.read_text(encoding="utf-8"))
    ids = {int(feature["properties"]["HSA93"]) for feature in data["features"]}
    if ids != classifications.keys():
        raise ValueError("CSV HSA IDs must match the GeoJSON HSA IDs.")

    for feature in data["features"]:
        properties = feature["properties"]
        value = classifications[int(properties["HSA93"])]
        properties["classification"] = value
        properties["fill"] = "#0000ff" if value == 1 else "#ff0000"
        properties["fill-opacity"] = 0.6

    GEOJSON.write_text(json.dumps(data, separators=(",", ":")) + "\n", encoding="utf-8")
    counts = Counter(classifications.values())
    print(f"Updated {len(ids)} HSAs: {counts[1]} blue, {counts[0] + counts[-1]} red.")


if __name__ == "__main__":
    main()
