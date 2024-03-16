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


# tool: clip raster by extent
RASTER_INPUT_FILE = ''
CLIP_BOUNDARY_FILE = ''
CLIP_RASTER_OUTPUT_FILE = ''

# tool: convert raster pixel to points
RASTER_INPUT_FILE = ''
OUT_POINT_FILE = ''


# tool: convert dn to radiance of satellite image bands
RASTER_INPUT_FILE = ''
RASTER_WORKING_DIR = ''
BANDS_LMAX_VALUES = [193.0, 365.0, 264.0, 221.0, 30.2, 16.5]
BANDS_LMIN_VALUES = [-1.520, -2.840, -1.170, -1.510, -0.370, -0.150]
QCAL_MIN_VALUE = 1
QCAL_MAX_VALUE = 255
OUT_NAME_PREFIX = 'band_'


# tool: export lulc individual class
LULC_RASTER_FILE = ''
LULC_OUT_CLASS_FILE = ''
LULC_CLASS_CODE = 1
