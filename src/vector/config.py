import os

from pathlib import Path
from consts import *
from src.vector.config_entity import *


class ConfigManager:
    def __init__(self):
        pass

    def get_point_config(self):
        point_config = PointConfig(
            inpoint=IN_POINT_FILE,
            single_point=SINGLE_POINT,
            point_offset=POINT_OFFSET_TO_GENERATE_GRID,
            point_file_coordinate_sys=POINT_FILE_COORDINATE_SYS
        )
        return point_config

    def get_polyline_config(self):
        polyline_config = PolylineConfig(
            inline=IN_POLYLINE_FILE,
            fnodeid=FNODE_FIELD_ID,
            tnodeid=TNODE_FIELD_ID,
            lineid=LINE_GEOM_ID,
            seqid=LINE_SEQUENCE_ID,
            is_xscl_available=IS_XSCL_EXIST,
            outxsclline=OUT_XSCL_POLYLINE_FILE,
            uidfield=OUT_UNIQUEID_FIELD,
            objectidfield=IN_XSCL_OBJECTID_FIELD,
            linefield=IN_XSCL_LINE_GEOMID_FIELD,
            interval=OUT_XSCL_INTERVAL,
            offset=OUT_XSCL_LINE_OFFSET,
            coordsys=IN_COORDINATE_SYS
        )
        return polyline_config

    def get_polygon_config(self):
        polygon_config = PolygonConfig(
            inpolygon=IN_POLYGON_FILE,
            cumfield_name=CUMULATIVE_AREA_FIELD_NAME,
            out_grid_polygon=OUT_GRID_POLYGON_FILE
        )
        return polygon_config

    def get_vectordata_config(self):
        vectordata_config = VectordataConfig(
            vector_outfile=VECTOR_OUT_FILE,
            vector_file_dir=VECTOR_FILE_DIR,
            vector_geometry_type=VECTOR_GEOMETRY_TYPE
        )
        return vectordata_config
