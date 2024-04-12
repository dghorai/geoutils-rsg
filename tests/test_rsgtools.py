"""
Test geoutils-rsg package.
"""


import os
import pandas as pd
import time

from rsgtools.vector_ops.create_grid_boundary import generate_grid_boundary
from rsgtools.raster_ops.clip_raster import clip_raster_by_extent
from rsgtools.vector_ops.find_nearest_point import get_nearest_point
from rsgtools.vector_ops.geometry_ops import CreateObjectID, CreateGroupID, GenerateHydroID
from rsgtools.vector_ops.create_crosssection_line import generate_river_xscl
from rsgtools.vector_ops.merge_vector_files import merge_shapefiles
from rsgtools.vector_ops.wkt_ops import WktUtils
from rsgtools.raster_ops.mosaic_large_geotiffs import mosaic_raster
from rsgtools import project_dir


def test_ClipRaster():
    # clip raster
    inRaster = os.path.join(project_dir, "notebooks/data/raster/SRTM_DEM.tif")
    inPolygon = os.path.join(
        project_dir, "notebooks/data/vector/clip_boundary.shp")
    out_raster = os.path.join(project_dir, "tests/results/clip_test.tif")
    clip_raster_by_extent(inRaster, inPolygon, out_raster)


def test_ClosestPoints():
    infc = os.path.join(
        project_dir, "notebooks/data/vector/sample_drainage_lines.shp")
    # get nearest point
    point = [84.4874, 18.8998]
    nearest_pnt = get_nearest_point(point, infc)


def test_OverlapArea():
    op = WktUtils()
    inwkts = os.path.join(project_dir, "notebooks/data/vector/sample_wkts.csv")
    # get overlap area
    wkt_df = pd.read_csv(inwkts)
    poly_overlap_nodes = op.extract_overlap_polygon(
        wkt_df['WKT'][0], wkt_df['WKT'][1])
    print(poly_overlap_nodes)


def test_GenerateIDs():
    # inputs
    infc = os.path.join(
        project_dir, "notebooks/data/vector/sample_drainage_lines.shp")
    # create line object id
    CreateObjectID(infc, fieldname="OBJECTID")
    # create line-connected group id
    CreateGroupID(infc, fieldname="GROUPID")
    # generate river line hydroid
    GenerateHydroID(infc, groupid="GROUPID", outfield="HYDROID")


def test_GenerateXSCLs():
    infc = os.path.join(
        project_dir, "notebooks/data/vector/sample_drainage_lines.shp")
    # generate perpendicular line at specific interval
    outfc = os.path.join(project_dir, "tests/results/out_cross_section.shp")
    generate_river_xscl(infc, outfc, "UID", 1000, 250)


def test_MergeShapefiles():
    # merge vector files
    filedir = os.path.join(project_dir, "notebooks/data/vector")
    outfile = os.path.join(project_dir, "tests/results/merge_lines.shp")
    merge_shapefiles(filedir, outfile, geometry_type='Line')


def test_MosaicGeotiffs():
    t0 = time.time()
    tiff_data_path = os.path.join(
        project_dir, "notebooks/data/raster/geotiff_tiles")
    mosaic_outfile = os.path.join(
        project_dir, "tests/results/mosaic_tiles.tif")
    mosaic_raster(tiff_data_path, mosaic_outfile)


def test_Point2Grid():
    # point to grid conversion
    inpoints = os.path.join(
        project_dir, "notebooks/data/vector/sample_grid_points.shp")
    outgrid = os.path.join(project_dir, "tests/results/point_to_grid.shp")
    generate_grid_boundary(inpoints, 5000, outgrid)
