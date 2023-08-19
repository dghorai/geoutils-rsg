import os

import src.rsgis.vector.find_nearest_point as fp

from src.logger import logging, project_dir


def main():
    infc = os.path.join(project_dir, "artifacts", "data",
                        "sample_drainage_lines.shp")
    # get nearest point
    point = [84.4874, 18.8998]
    nearest_pnt = fp.find_closest_point(point, infc)
    print(nearest_pnt)
