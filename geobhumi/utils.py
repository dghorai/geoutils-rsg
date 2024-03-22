# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Common functions for geospatial application.
"""

import os
import math
import random
import datetime
import numpy as np

from osgeo import ogr, osr, gdal, gdalconst
from ensure import ensure_annotations
from typing import Any
from geobhumi import CustomException, logger


@ensure_annotations
def dist_calc(p1: list, p2: list) -> float:
    """Calculate distance between two points"""
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


@ensure_annotations
def line_slope(p1: list, p2: list) -> Any:
    """Calculate slope of a line"""
    return "Inf" if p1[0] == p2[0] else ((p2[1]-p1[1])/(p2[0]-p1[0]))


def get_unique_field(layer):
    """Unique field in line shapefile"""

    lyr_definition = layer.GetLayerDefn()

    # check unique field id available or not
    field_names = []
    unqfieldname = None
    for n in range(lyr_definition.GetFieldCount()):
        field_name = lyr_definition.GetFieldDefn(n).GetName()

        if field_name == "OBJECTID":
            unqfieldname = field_name
        elif field_name == "SEGMENTID":
            unqfieldname = field_name
        else:
            unqfieldname = None

        field_names.append(field_name)

    return unqfieldname, field_names


def reading_polyline(inshp, shptype='polyline', fieldname=None, isnode=False):
    """Reading line shapefile"""

    nodes = []
    objects = []
    fdisc = {}
    if inshp.split(".")[-1] == 'shp':
        if shptype == 'line' or shptype == 'polyline':
            openfile = ogr.Open(inshp)
            # get layer
            layer = openfile.GetLayer(0)
            # check segmentid/objectid field exists or not
            unqfieldname, _ = get_unique_field(layer)

            if unqfieldname:
                for i in range(layer.GetFeatureCount()):
                    feature = layer.GetFeature(i)
                    geometry = feature.GetGeometryRef()
                    points = geometry.GetPoints()
                    objectid = feature.GetField(unqfieldname)

                    if fieldname:
                        fieldvalue = feature.GetField(fieldname)

                        if not fieldvalue in fdisc:
                            fdisc[fieldvalue] = []
                        fdisc[fieldvalue].append(
                            (objectid, points[0], points[-1]))

                    objects.append(objectid)
                    nodes.append(points)
            else:
                for i in range(layer.GetFeatureCount()):
                    objectid = i+1
                    feature = layer.GetFeature(i)
                    geometry = feature.GetGeometryRef()
                    points = geometry.GetPoints()

                    if fieldname:
                        fieldvalue = feature.GetField(fieldname)

                        if not fieldvalue in fdisc:
                            fdisc[fieldvalue] = []
                        fdisc[fieldvalue].append(
                            (objectid, points[0], points[-1]))

                    objects.append(objectid)
                    nodes.append(points)
        else:
            raise CustomException("File type other than polyline")
    else:
        raise CustomException("Invalid shapefile")

    # return results
    if fieldname != None:
        if isnode == True:
            return nodes, objects, fdisc
        else:
            return fdisc
    else:
        return objects, nodes


def writting_polyline(xylists, outfile, inlayer='', epsgno=0):
    """
    Create new line shapefile.
    """

    # Set up the shapefile driver
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # create the data source
    ds = driver.CreateDataSource(outfile)

    if len(inlayer) > 0:
        # get the spatial reference system
        srs = inlayer.GetSpatialRef()
        # create one layer
        layer = ds.CreateLayer("line", srs, ogr.wkbLineString)
    elif epsgno > 0:
        # create the spatial reference system
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsgno)
        # create one layer
        layer = ds.CreateLayer("line", srs, ogr.wkbLineString)
    else:
        raise CustomException(
            "SpatialReference not define, pass inlayer or epsgno arguments to the function")

    # Add an ID field
    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    layer.CreateField(idField)

    # Create the feature and set values
    featureDefn = layer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)

    # loop over line_list
    for n, xylist in enumerate(xylists):
        # Creating a line geometry
        linegeom = ogr.Geometry(ogr.wkbLineString)

        for x, y in xylist:
            linegeom.AddPoint(x, y)

        feature.SetGeometry(linegeom)
        feature.SetField("id", n+1)

    layer.CreateFeature(feature)
    feature = None

    # Save and close DataSource
    ds = None
    featureDefn.Destroy()

    return


def unique_and_newfield(layer, newfieldname, newfieldtype=ogr.OFTInteger):
    """Check unique field available or not and add a new field to line shapefile"""

    # check unique field id available or not
    unqfieldname, field_names = get_unique_field(layer)

    # check field if exists
    if newfieldname in field_names:
        fnfield = None
    else:
        fnfield = ogr.FieldDefn(newfieldname, newfieldtype)

    # create field if not available
    if fnfield:
        layer.CreateField(fnfield)

    return unqfieldname


@ensure_annotations
def line_fnt_nodes(line_nodes: list, segment_counts: list) -> tuple:
    """Generate start-node and end-node id of a line segment"""

    line_start_nodes = []
    line_end_nodes = []
    for cnt, nodes in enumerate(line_nodes):
        if nodes:
            line_start_nodes.append(nodes[0])
            line_end_nodes.append(nodes[-1])
        else:
            raise Exception("Invalid line segment id: {}".format(cnt+1))

    # find conected segment numbers
    objids = []
    nodeids = []
    for f, e in zip(segment_counts, line_end_nodes):
        for t, s in zip(segment_counts, line_start_nodes):
            if e == s:
                nodeids.append([f, f, t])
                objids.append(f)
                break

    # remove connected end-node segment ids from segment_counts to find terminal nodes
    terminal = [t for t in segment_counts if t not in objids]

    # assign node-ids to all terminal points
    max_obj_id = max(segment_counts)+1

    for j, m in enumerate(terminal):
        nodeids.append([m, m, j+max_obj_id])

    # return final nodeids
    return nodeids, terminal


def flip_line(layer):
    """Flip lines"""

    line_nodes = []
    rev_line_nodes = []
    rev_line_objid = []
    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        geom = feature.GetGeometryRef()
        pts = geom.GetPoints()
        line_nodes.append(pts)

    # loop over line_nodes
    for n, x in enumerate(line_nodes):
        ln = list()
        for r in reversed(x):
            ln.append(r)

        rev_line_nodes.append(ln)
        rev_line_objid.append(n+1)

    # return nodes
    return rev_line_objid, rev_line_nodes


def interval_points_straightline(p1, p2, interval=10):
    """Generate fixed interval points on straight line"""

    points = []
    if interval > 0:
        dist = dist_calc(p1, p2)
        m = line_slope(p1, p2)
        n = int(dist/interval)
        points.append(p2)

        for i in range(n):
            if p1[0] < p2[0] and p1[1] == p2[1]:
                ix = p2[0]-(interval*(i+1))
                iy = p2[1]
            elif p1[0] > p2[0] and p1[1] == p2[1]:
                ix = p2[0]+(interval*(i+1))
                iy = p2[1]
            elif p1[0] > p2[0] and p1[1] > p2[1]:
                ix = p2[0]+(interval*(i+1))/((1+m**2)**(0.5))
                iy = p2[1]+m*(ix-p2[0])
            elif p1[0] < p2[0] and p1[1] < p2[1]:
                ix = p2[0]-(interval*(i+1))/((1+m**2)**(0.5))
                iy = p2[1]+m*(ix-p2[0])
            elif p1[0] > p2[0] and p1[1] < p2[1]:
                ix = p2[0]+(interval*(i+1))/((1+m**2)**(0.5))
                iy = p2[1]+m*(ix-p2[0])
            elif p1[0] < p2[0] and p1[1] > p2[1]:
                ix = p2[0]-(interval*(i+1))/((1+m**2)**(0.5))
                iy = p2[1]+m*(ix-p2[0])
            elif p1[0] == p2[0] and p1[1] < p2[1]:
                ix = p2[0]
                iy = p2[1]-(interval*(i+1))
            elif p1[0] == p2[0] and p1[1] > p2[1]:
                ix = p2[0]
                iy = p2[1]+(interval*(i+1))
            else:
                break

            points.append([ix, iy])

        points.append(p1)
    else:
        raise Exception("interval not define")

    return points


def offset_random_point(lon, lat, offset=10, unit='km'):
    """Create a random point within given offset extent"""

    if offset > 0:
        if unit == 'km':
            # 1 degree = 111 km.
            a0 = offset*(1/111.0)
        else:
            raise Exception("convert offset to km.")

        # calc min and max axis
        x_min = lon - a0
        x_max = lon + a0
        y_min = lat - a0
        y_max = lat + a0

        # generate 1-random point withing the rectangular extent
        x_random = round(random.uniform(x_min, x_max), 6)
        y_random = round(random.uniform(y_min, y_max), 6)
    else:
        raise Exception("offset/distance not define")

    return x_random, y_random


def read_raster_as_array(rasterfile):
    imgDataSource = gdal.Open(rasterfile, gdalconst.GA_ReadOnly)
    geoTransform = imgDataSource.GetGeoTransform()
    rasterBands = imgDataSource.GetRasterBand()
    return rasterBands, geoTransform


def np2gdal_dtype(dtype=None):
    if dtype == 'uint16':
        res = gdal.GDT_UInt16
    elif dtype == 'uint32':
        res = gdal.GDT_UInt32
    elif dtype == 'int16':
        res = gdal.GDT_Int16
    elif dtype == 'int32':
        res = gdal.GDT_Int32
    elif dtype == 'float32':
        res = gdal.GDT_Float32
    elif dtype == 'float64':
        res = gdal.GDT_Float64
    elif dtype == 'cint16':
        res = gdal.GDT_CInt16
    elif dtype == 'cint32':
        res = gdal.GDT_CInt32
    elif dtype == 'cfloat32':
        res = gdal.GDT_CFloat32
    elif dtype == 'cfloat64':
        res = gdal.GDT_CFloat64
    else:
        raise CustomException("dtype not in the list")
    return res


def write_geotiff_file(arr, gt=None, sr=None, outfile_path=None, dtype=None):
    # check if file already exists
    if os.path.exists(outfile_path):
        os.remove(outfile_path)
    # check array dimension
    dim = arr.ndim
    # check no. of raster channels
    if dim == 3:
        nr, nc, n = arr.shape
    else:
        n = 1
        nr, nc = arr.shape
    # check output data type
    if dtype == None:
        dtype = gdal.GDT_UInt16
    # write output
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(outfile_path, nc, nr, n, dtype)
    outdata.SetGeoTransform(gt)  # specify coords
    outdata.SetProjection(sr)  # set projection
    # create raster
    if dim == 3:
        for b in range(n):
            outdata.GetRasterBand(b+1).WriteArray(arr[:, :, b])
    else:
        outdata.GetRasterBand(1).WriteArray(arr)
    outdata.FlushCache()  # saves to disk!!
    outdata = None
    return


def timeit(ptxt, timesec):
    sec = datetime.timedelta(seconds=int(timesec))
    dty = datetime.datetime(1, 1, 1) + sec
    if (dty.day - 1) > 0:
        dtxt = ("%d days %d hours %d minutes %d seconds" %
                (dty.day-1, dty.hour, dty.minute, dty.second))
    elif dty.hour > 0:
        dtxt = ("%d hours %d minutes %d seconds" %
                (dty.hour, dty.minute, dty.second))
    elif dty.minute > 0:
        dtxt = ("%d minutes %d seconds" % (dty.minute, dty.second))
    else:
        dtxt = ("%d seconds" % dty.second)
    logger.info(str(ptxt)+str(dtxt))
    return


def Histogram(arr, graylevel):
    arr[np.isinf(arr)] = 0
    arr[np.isnan(arr)] = 0
    width, height = arr.shape
    hist = [0]*(graylevel+1)  # say, graylevel = 256
    for y in range(height):
        for x in range(width):
            gray_level2 = arr[x, y]
            hist[gray_level2] = hist[gray_level2]+1
            del x
        del y
    return hist


def OTSU(arr, graylevel):
    hist = np.array(Histogram(arr, graylevel))
    bins = np.arange(graylevel+1)
    hist = hist.astype(float)
    # class probability for all possible thresholds
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # class means for all possible thresholds
    mean1 = np.cumsum(hist*bins)/weight1
    mean2 = (np.cumsum((hist*bins)[::-1])/weight2[::-1])[::-1]
    # clip ends to align class 1 and class 2 variables
    # the last value of weight1/mean1 should pair with zero values in weight2/mean2 which do not exist
    variance12 = weight1[:-1]*weight2[1:]*(mean1[:-1] - mean2[1:])**2
    idx = np.argmax(variance12)
    threshold = bins[:-1][idx]
    return threshold


def get_shapefile_epsg_code(in_shp):
    shp_ds = ogr.Open(in_shp)
    shp_lyr = shp_ds.GetLayer()
    src_epsg_code = int(shp_lyr.GetSpatialRef().GetAttrValue("AUTHORITY", 1))
    return src_epsg_code
