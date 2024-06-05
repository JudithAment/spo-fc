# Load packages
import os
import geopandas as gpd
import rioxarray as rxr
import numpy as np


# Define function
def estimate_emissions(ef_path, risk_path, proj_path):
    # Read project area
    project_area = gpd.read_file(proj_path)

    # Read ef & risk rasters masked by project area
    ef_per_ha = rxr.open_rasterio(
        ef_path,
        masked=True,
    ).rio.clip(project_area.geometry, project_area.crs, from_disk=True)

    risk_ha_per_pixel = rxr.open_rasterio(
        risk_path,
        masked=True,
    ).rio.clip(project_area.geometry, project_area.crs, from_disk=True)

    # Calculate emissions per pixel
    emissions_per_pixel = ef_per_ha * risk_ha_per_pixel

    # Sum emissions over project area
    total_emissions = np.nansum(emissions_per_pixel.values)

    return total_emissions


# Load data paths
q1_path = os.path.join("technical_exercise", "Question1")
ef_path = os.path.join(q1_path, "emissions_factor_strata.tif")
risk_path = os.path.join(q1_path, "ptest_risk_map_vp_clipped.tif")
proj_path = os.path.join(q1_path, "project_area.gpkg")

# Run estimation
print(estimate_emissions(ef_path, risk_path, proj_path))
#  1676.1728953037164