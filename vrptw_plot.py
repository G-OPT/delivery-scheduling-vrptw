import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, LineString
import contextily as ctx

# -----------------------------------------
# Load data
# -----------------------------------------
df = pd.read_csv("delivery_vrptw.csv")

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["lon"], df["lat"]),
    crs="EPSG:4326"
).to_crs(epsg=3857)

coords = {row["location"]: row.geometry for _, row in gdf.iterrows()}

# Example solution (you can update manually based on output from vrptw.py)
solution = {
    0: ["Depot", "C3", "C2", "Depot"],
    1: ["Depot", "C1", "C5", "C4", "Depot"]
}

colors = ["blue", "red", "green"]

fig, ax = plt.subplots(figsize=(10, 10))

# Plot each route
for v, stops in solution.items():
    points = [coords[s] for s in stops]
    line = LineString(points)

    gpd.GeoSeries([line], crs="EPSG:3857").plot(
        ax=ax, linewidth=3, color=colors[v], alpha=0.9, label=f"Vehicle {v}"
    )

    # arrows
    for i in range(len(points)-1):
        ax.annotate(
            "",
            xy=(points[i+1].x, points[i+1].y),
            xytext=(points[i].x, points[i].y),
            arrowprops=dict(arrowstyle="->", color=colors[v], lw=2)
        )

# Plot nodes
for _, row in gdf.iterrows():
    p = row.geometry
    name = row["location"]
    ax.scatter(p.x, p.y, s=120, color="black")
    ax.text(p.x + 50, p.y + 50, name, fontsize=10)

ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

plt.title("Delivery Scheduling VRPTW — G-OPT")
plt.legend()
plt.tight_layout()
plt.savefig("delivery_vrptw.png", dpi=300)
plt.show()
