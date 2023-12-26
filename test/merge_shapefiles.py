import os

import vector.merge_vector_files as mv

from logger import logging, project_dir


def main():
    # merge vector files
    filedir = os.path.join(project_dir, "artifacts", "data")
    outfile = os.path.join(project_dir, "test", "result", "merge_lines.shp")
    mv.merge_vector_files(outfile, filedir, geom_type='Line')
