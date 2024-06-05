import os
import numpy as np
import rioxarray as rxr
import pandas as pd

# Set data paths
q2_path = os.path.join("technical_exercise", "Question2")
t1_path = os.path.join(q2_path, "fnf_2008_clipped.tif")
t2_path = os.path.join(q2_path, "fnf_2011_clipped.tif")
t3_path = os.path.join(q2_path, "fnf_2014_clipped.tif")

# Define function
def generate_fcbm(t1_path, t2_path, t3_path):
    t1 = rxr.open_rasterio(t1_path, masked=True).squeeze()
    t2 = rxr.open_rasterio(t2_path, masked=True).squeeze()
    t3 = rxr.open_rasterio(t3_path, masked=True).squeeze()

    fcbm = t1.copy()

    fcbm.values[(t1.values == 2) & (t2.values == 2) & (t3.values == 2)] = 1
    fcbm.values[(t1.values == 2) & (t2.values == 2) & (t3.values == 1)] = 2
    fcbm.values[(t1.values == 2) & (t2.values == 1) & (t3.values == 2)] = 3
    fcbm.values[(t1.values == 2) & (t2.values == 1) & (t3.values == 1)] = 4
    fcbm.values[(t1.values == 1) & (t2.values == 1) & (t3.values == 1)] = 5
    fcbm.values[(t1.values == 1) & (t2.values == 2) & (t3.values == 2)] = 6
    fcbm.values[(t1.values == 1) & (t2.values == 2) & (t3.values == 1)] = 7
    fcbm.values[(t1.values == 1) & (t2.values == 1) & (t3.values == 2)] = 8

    return fcbm


# Run function to generate fcbm
fcbm = generate_fcbm(t1_path, t2_path, t3_path)

# Get number of pixels per transition value
transition_value, cell_count = np.unique(fcbm, return_counts=True)

# Translate number of pixels into ha
# ! only works for forest maps in projected crs with unit meter !
ha_per_cell = (fcbm.rio.resolution()[0] * -fcbm.rio.resolution()[1]) / 1e4
df = pd.DataFrame(
    np.asarray((transition_value, cell_count * ha_per_cell)).T,
    columns=["Transition Value", "Area (ha)"],
)

# Summarize by Interpreted Class for Use in UDef-A
class_lookup = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 3, 7: 3, 8: 4}
df["Interpreted Class"] = df["Transition Value"].map(class_lookup)
result = df.groupby("Interpreted Class")["Area (ha)"].sum().to_frame()

print(result)
#                    Area (ha)
# Interpreted Class
# 1                       8.10
# 2                   22490.73
# 3                       1.08
# 4                       0.09