import os

from pathlib import Path
from consts import *
from raster_ops.config_entity import *


class ConfigManager:
    def __init__(self):
        pass

    def get_rasterdata_config(self):
        rasterdata_config = RasterdataConfig(
            raster_infile=RASTER_INPUT_FILE,
            polygon_infile=CLIP_BOUNDARY_FILE,
            clip_raster_file=CLIP_RASTER_OUTPUT_FILE,
            out_point_file=OUT_POINT_FILE,
            output_folder=RASTER_WORKING_DIR,
            lmax_list=BANDS_LMAX_VALUES,
            lmin_list=BANDS_LMIN_VALUES,
            qcal_min=QCAL_MIN_VALUE,
            qcal_max=QCAL_MAX_VALUE,
            prefix=OUT_NAME_PREFIX,
            lulc_raster_file=LULC_RASTER_FILE,
            lulc_out_raster_file=LULC_OUT_CLASS_FILE,
            lilc_class_code=LULC_CLASS_CODE
        )
        return rasterdata_config
