import os

import vector.create_crosssection_line as gm

from logger import logging, project_dir


def main():
    infc = os.path.join(project_dir, "artifacts", "data",
                        "sample_drainage_lines.shp")
    # generate perpendicular line at specific interval
    outfc = os.path.join(project_dir, "test", "result",
                         "out_cross_section.shp")
    gm.construct_perpendicular_line(
        infc, outfc=outfc, interval=1000, offset=250, coordsys='GCS')
    gm.create_xscl_uniqueid(xscl_available=True, infc=infc, outfc=outfc,
                            uidfield="UID", interval=1000, offset=250, coordsys='GCS')
