# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Calculate cumulative drainage area.
"""

from osgeo import ogr


def get_polygon_area(seqdict, tnodedict, areadict):
    print(seqdict)
    newarea = {}
    for s2 in seqdict:
        if s2 in areadict:
            nArea = areadict[s2]
        if s2 in tnodedict:
            a1 = []
            for s3 in tnodedict[s2]:
                v1 = areadict[s3][0]
                a1.append(v1)
            v2 = nArea+a1
            v3 = sum(v2)
            if not s2 in newarea:
                newarea[s2] = []
            newarea[s2].append(v3)
    return newarea


def iter_polygon_area(seqdict, tnodedict, areadict):
    na = get_polygon_area(seqdict, tnodedict, areadict)
    for k1 in areadict.keys():
        for k2 in na.keys():
            if k1 == k2:
                areadict[k1] = na[k2]
    return areadict


def cumulative_drainage_area(inline, inpolygon, fnodeid="FNODE", tnodeid="TNODE", lineid="LINEID", seqid="SEQID", cumfield_name="CUMAREA"):
    """calculate drainage area"""
    seqdict = {}
    tnodedict = {}
    rShapefile = ogr.Open(inline)
    rLayer = rShapefile.GetLayer(0)
    for i in range(rLayer.GetFeatureCount()):
        feature = rLayer.GetFeature(i)
        fnode = feature.GetField(fnodeid)
        tnode = feature.GetField(tnodeid)
        line = feature.GetField(lineid)
        seqs = feature.GetField(seqid)
        # dict
        if not seqs in seqdict:
            seqdict[seqs] = []
        seqdict[seqs].append(line)
        # dict
        if not tnode in tnodedict:
            tnodedict[tnode] = []
        tnodedict[tnode].append(fnode)

    # read polygon file
    areadict = {}
    tShapefile = ogr.Open(inpolygon)
    tLayer = tShapefile.GetLayer(0)
    for j in range(tLayer.GetFeatureCount()):
        feat = tLayer.GetFeature(j)
        plyid = feat.GetField(lineid)
        geom = feat.GetGeometryRef()
        area = geom.GetArea()
        if not plyid in areadict:
            areadict[plyid] = []
        areadict[plyid].append(area)

    # calc cumulative area
    temp_area = []
    for k in seqdict.keys():
        orderid = seqdict[k]
        next_area = get_polygon_area(orderid, tnodedict, areadict)
        next_dict = iter_polygon_area(areadict, tnodedict, next_area)
        areadict = next_dict
        temp_area.append(next_dict)

    # return final cumulative area
    newAreaDict = temp_area[-1]

    # update field
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(inpolygon, 1)
    lyr = dataSource.GetLayer()
    # create fileds
    cumfield = ogr.FieldDefn(cumfield_name, ogr.OFTReal)
    lyr.CreateField(cumfield)
    for u in range(lyr.GetFeatureCount()):
        feat = lyr.GetFeature(u)
        obj = feat.GetField(lineid)
        if obj in newAreaDict:
            feat.SetField(cumfield_name, newAreaDict[obj][0])
            lyr.SetFeature(feat)
    # flash
    dataSource.Destroy()


# if __name__ == "__main__":
#     inRiver = r"E:\Education\River_Line.shp"
#     inCatchment = r"E:\Education\Catchment_Boundary.shp"
#     cumulative_drainage_area(inRiver, inCatchment, cumfield_name="CatchmentArea")
