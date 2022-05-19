# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Common functions for geometry operation in GIS.
"""

import math
import random

from osgeo import ogr, osr


class CommonUtils:
    """
    Common functions for polyline geometry operation.
    """
    def __init__(self):
        """constructure"""
    
    def dist_calc(self, p1, p2):
        """Calculate distance between two points"""
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    
    def line_slope(self, p1, p2):
        """Calculate slope of a line"""
        if p1[0] == p2[0]:
            m = "Inf"
        else:
            m = ((p2[1]-p1[1])/(p2[0]-p1[0]))
        return m
    
    def get_unique_field(self, layer):
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

    def reading_polyline(self, inshp, shptype='polyline', fieldname=None, isnode=False):
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
                unqfieldname, _ = self.get_unique_field(layer)
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
                            fdisc[fieldvalue].append((objectid, points[0], points[-1]))
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
                            fdisc[fieldvalue].append((objectid, points[0], points[-1]))
                        objects.append(objectid)
                        nodes.append(points)
            else:
                raise Exception("File type other than polyline")
        else:
            raise Exception("Invalid shapefile")

        # return results
        if fieldname != None:
            if isnode == True:
                return nodes, objects, fdisc
            else:
                return fdisc
        else:
            return objects, nodes
    
    def writting_polyline(self, xylists, outfile, inlayer='', epsgno=0):
        """
        Create new line shapefile.
        Reference: 
        (1) https://gis.stackexchange.com/questions/392515/create-a-shapefile-from-geometry-with-ogr
        (2) https://www.gis.usu.edu/~chrisg/python/2009/lectures/ospy_slides2.pdf
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
            srs =  osr.SpatialReference()
            srs.ImportFromEPSG(epsgno)
            # create one layer 
            layer = ds.CreateLayer("line", srs, ogr.wkbLineString)
        else:
            raise Exception("SpatialReference not define, pass inlayer or epsgno arguments to the function")
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

    def unique_and_newfield(self, layer, newfieldname, newfieldtype=ogr.OFTInteger):
        """Check unique field available or not and add a new field to line shapefile"""
        # check unique field id available or not
        unqfieldname, field_names = self.get_unique_field(layer)
        # check field if exists
        if newfieldname in field_names:
            fnfield = None
        else:
            fnfield = ogr.FieldDefn(newfieldname, newfieldtype)
        # create field if not available
        if fnfield:
            layer.CreateField(fnfield)
        return unqfieldname
    
    def line_fnt_nodes(self, line_nodes, segment_counts):
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

    def flip_line(self, layer):
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
    
    def fixed_interval_points(self, infc, interval, flipline=False, save=False, outfc=None, lineslope=False):
        """Generate fixed interval points along polyline.
        Reference: 
        (1) http://nodedangles.wordpress.com/2011/05/01/quick-dirty-arcpy-batch-splitting-polylines-to-a-specific-length/
        (2) https://github.com/HeyHarry3636/CrossSections_python/blob/master/crossSections_05262016.py

        """
        def mid_point(p1, p2, l1, l2):
            iX = p1[0]+((p2[0]-p1[0])*(l1/l2))
            iY = p1[1]+((p2[1]-p1[1])*(l1/l2))
            pts = [iX, iY]
            return pts
        
        # get nodes and objectids
        if flipline == True:
            openfile = ogr.Open(infc)
            in_layer = openfile.GetLayer(0)
            objects, nodes = self.flip_line(in_layer)
        else:
            objects, nodes = self.reading_polyline(infc)

        # generate points
        points = []
        slopes = []
        for n, i in zip(objects, nodes):
            tDist = 0 # total distance
            vPoint = None # previous point
            for pnt in i:
                if not (vPoint is None):
                    thisDist = self.dist_calc(vPoint, pnt)
                    maxAddDist = interval - tDist
                    if (tDist+thisDist) > interval:
                        pCnt = int((tDist+thisDist)/interval)
                        for k in range(pCnt):
                            maxAddDist = interval - tDist
                            nPoint = mid_point(vPoint, pnt, maxAddDist, thisDist)
                            slope = self.line_slope(vPoint, nPoint)
                            points.append(nPoint+[n])
                            slopes.append(slope)
                            vPoint = nPoint
                            thisDist = self.dist_calc(vPoint, pnt)
                            tDist = 0
                        tDist += thisDist
                    else:
                        tDist += thisDist
                else:
                    tDist = 0
                vPoint = pnt

        # save if needed
        if save == True:
            openfile = ogr.Open(infc)
            in_layer = openfile.GetLayer(0)
            srs = in_layer.GetSpatialRef()
            driver = ogr.GetDriverByName('ESRI Shapefile')
            shapeData = driver.CreateDataSource(outfc)
            out_layer = shapeData.CreateLayer('point', srs, ogr.wkbPoint)
            # create fileds
            lineid = ogr.FieldDefn("LINEID", ogr.OFTInteger)
            out_layer.CreateField(lineid)
            pointid = ogr.FieldDefn("POINTID", ogr.OFTInteger)
            out_layer.CreateField(pointid)
            lyrDef = out_layer.GetLayerDefn()
            # Create point
            for n, p in enumerate(points):
                pt = ogr.Geometry(ogr.wkbPoint)
                pt.SetPoint(0, p[0], p[1])
                feature = ogr.Feature(lyrDef)
                feature.SetGeometry(pt)
                feature.SetField("POINTID", n+1)
                feature.SetField("LINEID", p[2])
                out_layer.CreateFeature(feature)
            # Flush
            shapeData.Destroy()
        
        # return points
        if lineslope == True:
            return points, slopes
        else:
            return points
    
    def intersect_point_to_line(self, point, line_start, line_end):
        """
        Find intersect point.
        Source: https://gis.stackexchange.com/questions/396/nearest-neighbor-between-point-layer-and-line-layer
        """
        line_magnitude = self.dist_calc(line_end, line_start)
        u = ((point[0]-line_start[0])*(line_end[0]-line_start[0])+(point[1]-line_start[1])*(line_end[1]-line_start[1]))/(line_magnitude**2)
        # Closest point does not fall within the line segment, take the shorter distance to an endpoint
        if u < 0.00001 or u > 1:
            ix = self.dist_calc(point, line_start)
            iy = self.dist_calc(point, line_end)
            if ix > iy:
                return line_end
            else:
                return line_start
        else:
            ix = line_start[0]+u*(line_end[0]-line_start[0])
            iy = line_start[1]+u*(line_end[1]-line_start[1])
            return ix, iy
    
    def interval_points_straightline(self, p1, p2, interval=10):
        """Generate fixed interval points on straight line"""
        points = []
        if interval > 0:
            dist = self.dist_calc(p1, p2)
            m = self.line_slope(p1, p2)
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

    
    def offset_random_point(self, lon, lat, offset=10, unit='km'):
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
    
    def BBoxIntersect(self, lyr1Ext, lyr2Ext):
        """
        Bounding Box intersection test.
        Source: https://gis.stackexchange.com/questions/57964/get-vector-features-inside-a-specific-extent
        """
        # lyr1Ext - reference layer
        b1_x = lyr1Ext[0]
        b1_y = lyr1Ext[2]
        b1_w = lyr1Ext[1] - lyr1Ext[0] # Horizontal length
        b1_h = lyr1Ext[3] - lyr1Ext[2] # Vertical length
        # lyr2Ext - clip/intersect layer
        b2_x = lyr2Ext[0]
        b2_y = lyr2Ext[2]
        b2_w = lyr2Ext[1] - lyr2Ext[0] # horizontal length
        b2_h = lyr2Ext[3] - lyr2Ext[2] # vertical length
        # query for select object which is inside of the reference extent
        if (b1_x > b2_x + b2_w - 1) or (b1_y > b2_y + b2_h - 1) or (b2_x > b1_x + b1_w - 1) or (b2_y > b1_y + b1_h - 1):
            return False
        else:
            return True
    
    


