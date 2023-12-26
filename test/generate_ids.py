# import modules
import os

import rsgis.vector.line_geometry as pg

from logger import logging, project_dir


def main():
    # inputs
    infc = os.path.join(project_dir, "artifacts", "data",
                        "sample_drainage_lines.shp")
    # create line object id
    pg.CreateObjectID(infc, fieldname="OBJECTID")
    # create line-connected group id
    pg.CreateGroupID(infc, fieldname="GROUPID")
    # generate river line hydroid
    pg.GenerateHydroID(infc, groupid="GROUPID", outfield="HYDROID")
