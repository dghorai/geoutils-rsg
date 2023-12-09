from pathlib import Path

# input vector file
IN_POINT_FILE = ''
IN_POLYLINE_FILE = ''
IN_POLYGON_FILE = ''


# tool: cumulative drainage area calculation
FNODE_FIELD_ID = "FNODE"
TNODE_FIELD_ID = "TNODE"
LINE_GEOM_ID = "LINEID"
LINE_SEQUENCE_ID = "SEQID"
CUMULATIVE_AREA_FIELD_NAME = "CUMAREA"


# tool: generate cross-section-cut-line
IS_XSCL_EXIST = False
IN_XSCL_OBJECTID_FIELD = "OBJECTID"
IN_XSCL_LINE_GEOMID_FIELD = "LINEID"
IN_COORDINATE_SYS = 'GCS'
OUT_XSCL_POLYLINE_FILE = ''
OUT_UNIQUEID_FIELD = "UID"
OUT_XSCL_INTERVAL = 500
OUT_XSCL_LINE_OFFSET = 500


# tool: find nearest point between a single point and polyline-network
SINGLE_POINT = (80.5, 22.5)


# tool: merge vector files
VECTOR_OUT_FILE = ''
VECTOR_FILE_DIR = ''
VECTOR_GEOMETRY_TYPE = 'Point'  # Point/Line/Polygon


# tool: create grid polygon from point file
OUT_GRID_POLYGON_FILE = ''
POINT_OFFSET_TO_GENERATE_GRID = 500
POINT_FILE_COORDINATE_SYS = 'GCS'
