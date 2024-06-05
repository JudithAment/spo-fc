# Load packages
import os
import rioxarray as rxr
import geopandas as gpd
from rasterstats import zonal_stats

def estimate_emissions(ef_path, risk_path, proj_path):
    ef = rxr.open_rasterio(ef_path, masked=True).squeeze()
    risk = rxr.open_rasterio(risk_path, masked=True).squeeze()
    project_area = gpd.read_file(proj_path)

    # Test crs, extent, resolution
    if (
        (ef.rio.crs == risk.rio.crs)
        & (ef.rio.bounds() == risk.rio.bounds())
        & (ef.shape == risk.shape)
        & (ef.rio.resolution() == risk.rio.resolution())
    ):
        # Calculate emissions
        emissions = ef * risk

        # Mean emissions in project area in CO2e/ha
        mean_emissions = zonal_stats(
            project_area,
            emissions.values,
            affine=emissions.rio.transform(),
            stats="mean",
        )[0]["mean"]

        # Get project area in ha
        # project_area = project_area.to_crs("+proj=cea")  # this does not work..

        # Multiply area by mean emissions
        est_emissions = project_area.area[0] / 1e4 * mean_emissions

        return est_emissions

    else:
        print(
            "Risk and emissions maps do not have the same crs, extent, resolution or shape. Need to reproject or resample first"
        )

# Load data
q1_path = os.path.join("technical_exercise", "Question1")
ef_path = os.path.join(q1_path, "emissions_factor_strata.tif")
risk_path = os.path.join(q1_path, "ptest_risk_map_vp_clipped.tif")
proj_path = os.path.join(q1_path, "project_area.gpkg")

estimate_emissions(ef_path, risk_path, proj_path)
