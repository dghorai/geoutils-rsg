from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class PointConfig:
    inpoint: Path
    single_point: tuple
    point_offset: float
    point_file_coordinate_sys: str


@dataclass(frozen=True)
class PolylineConfig:
    inline: Path
    fnodeid: str
    tnodeid: str
    lineid: str
    seqid: str
    is_xscl_available: bool
    outxsclline: Path
    uidfield: str
    objectidfield: str
    linefield: str
    interval: int
    offset: int
    coordsys: str


@dataclass(frozen=True)
class PolygonConfig:
    inpolygon: Path
    cumfield_name: str
    out_grid_polygon: Path


@dataclass(frozen=True)
class VectordataConfig:
    vector_outfile: Path
    vector_file_dir: Path
    vector_geometry_type: str
