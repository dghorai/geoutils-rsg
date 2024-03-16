from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class RasterdataConfig:
    raster_infile: Path
    polygon_infile: Path
    clip_raster_file: Path
    out_point_file: Path
    output_folder: Path
    lmax_list: list
    lmin_list: list
    qcal_min: float
    qcal_max: float
    prefix: str
    lulc_raster_file: Path
    lulc_out_raster_file: Path
    lilc_class_code: int
