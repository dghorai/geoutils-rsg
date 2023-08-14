import os
import pandas as pd

from rsgis.logger import logging, project_dir
from rsgis.vector.wkt_ops import WktUtils


def main():
    op = WktUtils()
    inwkts = os.path.join(project_dir, "data", "sample_wkts.csv")
    # get overlap area
    wkt_df = pd.read_csv(inwkts)
    poly_overlap_nodes = op.extract_overlap_polygon(
        wkt_df['WKT'][0], wkt_df['WKT'][1])
    print(poly_overlap_nodes)
