# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Common functions for geometry operation in GIS.
"""

import math
import random


from osgeo import ogr, osr, gdal, gdalconst
from ensure import ensure_annotations
from typing import Any
from exception import CustomException


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
