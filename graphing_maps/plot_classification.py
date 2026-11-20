"""Plot original HSA classifications for the contiguous United States."""

from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


MAP_DIR = Path(__file__).resolve().parent
ROOT = MAP_DIR.parent
GEOJSON = ROOT / "HSA_Bdry__AK_HI_unmodified/hsa-geojson/HsaBdry_AK_HI_unmodified.geojson"
COLORS = {-1: "#0080ff", 0: "#d9d9d9", 1: "#d73027"}


def main():
    classifications = pd.read_csv(ROOT / "hsa_classifications.csv")
    if classifications.HSA93.duplicated().any():
        raise ValueError("Duplicate HSA IDs in classification CSV.")
    if not classifications.classification.isin(COLORS).all():
        raise ValueError("Classifications must be -1, 0, or 1.")

    hsas = gpd.read_file(GEOJSON).to_crs("EPSG:4326")
    hsas["HSA93"] = hsas["HSA93"].astype(int)
    labels = classifications.set_index("HSA93")["classification"]
    hsas["original_classification"] = hsas["HSA93"].map(labels)
    if hsas.original_classification.isna().any():
        raise ValueError("Some GeoJSON HSAs have no CSV classification.")
    # Match the prediction figure's extent, projection, and dimensions.
    hsas = hsas.cx[-125:-66, 24:50].to_crs("EPSG:5070")
    fig, ax = plt.subplots(figsize=(10, 6))
    hsas.plot(ax=ax, color=hsas.original_classification.map(COLORS),
              edgecolor="white", linewidth=0.15)
    ax.set_axis_off()
    ax.legend(handles=[
        Patch(facecolor=COLORS[-1], label="Coldspot"),
        Patch(facecolor=COLORS[1], label="Hotspot"),
        Patch(facecolor=COLORS[0], label="Not statistically significant"),
    ], loc="lower left", frameon=False, fontsize=9)
    fig.savefig(MAP_DIR / "classification_map.pdf", bbox_inches="tight")
    fig.savefig(MAP_DIR / "classification_map.png", dpi=600, bbox_inches="tight")
    plt.close(fig)
    print("Saved classification_map.pdf and classification_map.png")


if __name__ == "__main__":
    main()
