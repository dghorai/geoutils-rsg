# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:08:54 2019

@author: Debabrata Ghorai, Ph.D.

Objective: Mosaic large GeoTiff files using GDAL and Python extension package with less time
"""

import os
import time

from raster.mosaic_large_geotiffs import LargeGeoTiffMosaic
from logger import project_dir


def main():
    t0 = time.time()
    tiff_data_path = os.path.join(
        project_dir, "artifacts", "data", "geotiff_tiles")
    mosaic_outfile = os.path.join(
        project_dir, "test", "result", "mosaic_tiles.tif")
    mos = LargeGeoTiffMosaic()
    mos.mosaic_raster_tiles(tiff_data_path, mosaic_outfile)
    mos.print_time_taken("Total time: ", time.time() - t0)
