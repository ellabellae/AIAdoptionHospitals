from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

MAP_DIR = Path(__file__).resolve().parent
ROOT = MAP_DIR.parent
path = ROOT / "HSA_Bdry__AK_HI_unmodified/hsa-geojson/predicted_results.geojson"
hsas = gpd.read_file(path).to_crs("EPSG:4326")

# mainland US only
hsas = hsas.cx[-125:-66, 24:50].to_crs("EPSG:5070")

fig, ax = plt.subplots(figsize=(10, 6))
hsas.plot(
    ax=ax,
    color=hsas["fill"],
    edgecolor="white",
    linewidth=0.15,
)
ax.set_axis_off()

legend = [
    Patch(facecolor="#0080ff", label="Correct coldspot"),
    Patch(facecolor="#4602FF", label="Coldspot predicted as hotspot"),
    Patch(facecolor="#B863F1", label="Hotspot predicted as coldspot"),
    Patch(facecolor="#d73027", label="Correct hotspot"),
    Patch(facecolor="#d9d9d9", label="No held-out prediction"),
]
ax.legend(
    handles=legend,
    loc="lower left",
    frameon=False,
    fontsize=9,
)

fig.savefig(MAP_DIR / "prediction_map.pdf", bbox_inches="tight")
fig.savefig(MAP_DIR / "prediction_map.png", dpi=600, bbox_inches="tight")
plt.close(fig)