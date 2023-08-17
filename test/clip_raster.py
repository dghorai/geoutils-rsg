import os

import src.rsgis.raster.clip_raster as clip
from src.logger import logging, project_dir


def main():
    # clip raster
    inRaster = os.path.join(project_dir, "data", "sample_raster_dem.tif")
    inPolygon = os.path.join(project_dir, "data", "clip_boundary.shp")
    clip_raster = clip.ClipRaster(inRaster, inPolygon)
    result_array = clip_raster.subset_by_extent()
    print(result_array)
