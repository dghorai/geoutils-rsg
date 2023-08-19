import os

import src.rsgis.vector.point_to_square_polygon as grd

from src.logger import logging, project_dir


def main():
    # point to grid conversion
    inpoints = os.path.join(project_dir, "artifacts",
                            "data", "sample_grid_points.shp")
    outgrid = os.path.join(project_dir, "test", "result", "point_to_grid.shp")
    grd.point_to_grid(inpoints, outgrid, offset=5000, coordsys='GCS')
