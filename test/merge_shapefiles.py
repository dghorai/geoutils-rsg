import os

import rsgis.vector.merge_vector_files as mv

from rsgis.logger import logging, project_dir


def main():
    # merge vector files
    filedir = os.path.join(project_dir, "data")
    outfile = os.path.join(project_dir, "test", "result", "merge_lines.shp")
    mv.merge_vector_files(outfile, filedir, geom_type='Line')
