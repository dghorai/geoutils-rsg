# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Generate perpendicular line along polyline at specific interval and
assign uniqueid to the perpendicular lines.
"""

import os
import math

from osgeo import ogr

from rsgis.utils import CommonUtils

comt = CommonUtils()


def construct_perpendicular_line(infc, outfc=None, interval=500, offset=500, save=True, coordsys='GCS'):
    """Construct perpendicular line"""
    if coordsys == 'GCS':
        # assuming units are in meter
        interval = interval*(1/(111.0*1000))
        offset = offset*(1/(111.0*1000))

    objids = []
    lineids = []
    try:
        # generate perpendicular line nodes
        iPts, iSlp = comt.fixed_interval_points(
            infc, interval, flipline=True, lineslope=True)

        xscl = list()
        for i, j in zip(iPts, iSlp):
            if j == 0.0 or j == -0.0:
                p1 = i[0], i[1]+offset
                p2 = i[0], i[1]-offset
            elif j == "Inf":
                p1 = i[0]+offset, i[1]
                p2 = i[0]-offset, i[1]
            elif j != 0 and j != "Inf":
                dx = offset/math.sqrt(1+(1/j**2))
                dy = offset/(j*math.sqrt(1+(1/j**2)))
                p1 = i[0]+dx, i[1]-dy
                p2 = i[0]-dx, i[1]+dy
            else:
                print("Extra Point:", i, j)
            v1 = p1, p2, i[2]
            xscl.append(v1)

        if save == True:
            # perpendicular lines creation
            shapefile = ogr.Open(infc)
            layer = shapefile.GetLayer(0)
            spr = layer.GetSpatialRef()
            spr.ExportToWkt()
            driver = ogr.GetDriverByName('ESRI Shapefile')
            if os.path.exists(outfc):
                driver.DeleteDataSource(outfc)
            shapeData = driver.CreateDataSource(outfc)
            lyr = shapeData.CreateLayer(
                'myLyr2', spr, geom_type=ogr.wkbMultiLineString)
            # create fileds
            lineid = ogr.FieldDefn("LINEID", ogr.OFTInteger)
            lyr.CreateField(lineid)
            objectid = ogr.FieldDefn("OBJECTID", ogr.OFTInteger)
            lyr.CreateField(objectid)
            lyrDef = lyr.GetLayerDefn()
            for ix, row in enumerate(xscl):
                s, e, n = row[0], row[1], row[2]
                line = ogr.Geometry(ogr.wkbLineString)
                line.AddPoint(s[0], s[1])
                line.AddPoint(e[0], e[1])
                feature = ogr.Feature(lyrDef)
                feature.SetGeometry(line)
                feature.SetField("OBJECTID", ix+1)
                feature.SetField("LINEID", n)
                lyr.CreateFeature(feature)
            # Flush
            shapeData.Destroy()
        else:
            for ix, row in enumerate(xscl):
                n = row[2]
                objids.append([n, ix+1])
                lineids.append(n)
    except Exception as e:
        print(e)

    # return
    if save == False:
        return objids, lineids


def create_xscl_uniqueid(xscl_available=False, infc=None, outfc=None, uidfield="UID", objectidfield="OBJECTID", linefield="LINEID", interval=500, offset=500, coordsys='GCS'):
    """Assign uniqueid to perpendicular line"""
    if xscl_available == True:
        if outfc:
            objids = []
            lineids = []
            shapefile = ogr.Open(outfc)
            layer = shapefile.GetLayer(0)
            for row in range(layer.GetFeatureCount()):
                feature = layer.GetFeature(row)
                objid = feature.GetField(objectidfield)
                lineid = feature.GetField(linefield)
                objids.append([lineid, objid])
                lineids.append(lineid)
        else:
            raise Exception("outfc not provided")
    else:
        construct_perpendicular_line(
            infc=infc, outfc=outfc, interval=interval, offset=offset, coordsys=coordsys)
        objids, lineids = construct_perpendicular_line(
            infc=infc, interval=interval, offset=offset, save=False, coordsys=coordsys)

    # get unique lineids
    unqlineids = list(set(lineids))
    comid = []
    for i in unqlineids:
        v2 = []
        for j in objids:
            if i == j[0]:
                v2.append(j[1])
        comid.append([i, v2])

    # write shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(outfc, 1)
    outlyr = dataSource.GetLayer()
    defn = outlyr.GetLayerDefn()
    if defn.GetFieldIndex(uidfield) == -1:
        # create fileds
        outlyr.CreateField(ogr.FieldDefn(uidfield, ogr.OFTString))
    # feat_def.AddFieldDefn(uidfield)
    for u in range(outlyr.GetFeatureCount()):
        feat = outlyr.GetFeature(u)
        objid = feat.GetField(objectidfield)
        for k in comid:
            for l in range(len(k[1])):
                if objid == k[1][l]:
                    new_id = str(k[0])+"_"+str(l)
                    feat.SetField(uidfield, new_id)
                    outlyr.SetFeature(feat)
    # Flush
    dataSource.Destroy()
    return "Process Completed!"
