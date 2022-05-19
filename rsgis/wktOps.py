# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

WKT related operation.
"""

import math
import warnings

import pandas as pd
import geopandas as gpd
import numpy as np
from pyproj import Proj
from scipy.spatial import ConvexHull

warnings.filterwarnings(action='ignore')

class WktUtils:
    """
    A class for common and useful GIS tools.
    This class consisting of several GIS functions and this functions using as a helper function
    for various geospatial application development.
    """

    def __init__(self):
        """constructor"""
        # 1 m2 = 0.000247105 acre
        self.sqm2acre = 0.000247105

    def wkt_to_gdf(self, wkts, crs='epsg:4326'):
        """Create WKT string to GeoDataFrame"""
        # geom_str to geodataframe
        df = pd.DataFrame([wkts], columns=['geometry'])
        df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
        gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=crs)
        return gdf

    def wkt_vertices(self, wkts):
        """Extract nodes of a WKT"""
        coords_list_fn = None
        if type(wkts) == str:
            print('Input is wkt string')
            if wkts.split()[0] == 'POLYGON':
                # extract all coordinates from wkt
                coords_str = wkts.strip().replace('POLYGON ((', '').replace('))', '').split(',')
                coords_list = [[float(i) for i in ii.split()] for ii in coords_str]
                if coords_list[0] == coords_list[-1]:
                    coords_list_fn = coords_list
                else:
                    coords_list_fn = []
                    raise Exception("Invalid WKT or polygon not closed.")
            else:
                coords_list_fn = []
                raise TypeError("Only POLYGON types are allowed or WKT string may be incorrect.")
        else:
            print('Input is geodataframe')
            # Extract nodes from GeoDataFrame
            g = [i for i in wkts.geometry]
            x, y = g[0].exterior.coords.xy
            coords_list_fn = np.dstack((x, y)).tolist()
        return coords_list_fn
    
    def line_intersection(self, line1, line2):
        """
        Return a (x, y) tuple or None if there is no intersection.
        Source: https://rosettacode.org/wiki/Find_the_intersection_of_two_lines#Python
        """
        Ax1, Ay1, Ax2, Ay2 = sum(line1, [])
        Bx1, By1, Bx2, By2 = sum(line2, [])
        # calc difference
        d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
        ix = None
        if abs(d) > 0:
            uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
            uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        else:
            ix = None
        # check outer extent
        if not (0 <= uA <= 1 and 0 <= uB <= 1):
            ix = None
        x = Ax1 + uA * (Ax2 - Ax1)
        y = Ay1 + uA * (Ay2 - Ay1)
        ix = x, y
        # return final intersected point (x, y)
        return ix
    
    def ray_tracing_method(self, point, poly):
        """
        Checking if a point or node is inside a polygon.
        Source: https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
        """
        x, y = point
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n+1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside
    
    def sort_counter_clockwise(self, points):
        """
        Sort a list of points in counter clockwise.
        Source: https://stackoverflow.com/questions/69100978/how-to-sort-a-list-of-points-in-clockwise-anti-clockwise-in-python
        """
        centre_x = sum([i[0] for i in points])/len(points) 
        centre_y = sum([i[1] for i in points])/len(points)
        angles = [math.atan2(y - centre_y, x - centre_x) for x, y in points]
        cc_indices = sorted(range(len(points)), key=lambda i: angles[i])
        cc_points = [points[i] for i in cc_indices]
        return cc_points
    
    def latlon_to_utm(self, lon, lat):
        """
        Convert lat/long to UTM unit.
        Source: https://linuxtut.com/en/4cdf303493d73e24dc14/
        """
        # Compute UTM zone
        utm_zone = int(divmod(lon, 6)[0])+31
        # Defime DD2UTM converter
        dd_to_utm = Proj(proj='utm', zone=utm_zone, ellps='WGS84')
        # Apply the converter
        utm_x, utm_y = dd_to_utm(lon, lat)
        # Add offset if the point in the southern hemisphere
        if lat < 0:
            utm_y = utm_y+10000000
        dd2utm = [utm_x, utm_y, utm_zone]
        return dd2utm
    
    def minimum_bounding_rectangle(self, points):
        """
        Find the minimum area rectangle.
        Source: https://stackoverflow.com/questions/13542855/algorithm-to-find-the-minimum-area-rectangle-for-given-points-in-order-to-comput
        """
        pi2 = np.pi/2.0
        # get the convex hull for the point list
        vertices_index = list(ConvexHull(points).vertices)
        hull_points = np.array([points[i] for i in vertices_index])
        # calculate edge angles
        edges = hull_points[1:] - hull_points[:-1]
        angles = np.arctan2(edges[:, 1], edges[:, 0])
        angles = np.unique(np.abs(np.mod(angles, pi2)))
        # find rotation matrices
        rotations = np.vstack([np.cos(angles), np.cos(angles-pi2), np.cos(angles+pi2), np.cos(angles)]).T
        rotations = rotations.reshape((-1, 2, 2))
        # apply rotations to the hull
        rot_points = np.dot(rotations, hull_points.T)
        # find the bounding points
        min_x = np.nanmin(rot_points[:, 0], axis=1)
        max_x = np.nanmax(rot_points[:, 0], axis=1)
        min_y = np.nanmin(rot_points[:, 1], axis=1)
        max_y = np.nanmax(rot_points[:, 1], axis=1)
        # find the box with the best area
        areas = (max_x - min_x) * (max_y - min_y)
        best_idx = np.argmin(areas)
        # return the best box
        x1 = max_x[best_idx]
        x2 = min_x[best_idx]
        y1 = max_y[best_idx]
        y2 = min_y[best_idx]
        r = rotations[best_idx]
        # final rectangle-nodes for close polygon
        rval = np.zeros((5, 2))
        rval[0] = np.dot([x1, y2], r)
        rval[1] = np.dot([x2, y2], r)
        rval[2] = np.dot([x2, y1], r)
        rval[3] = np.dot([x1, y1], r)
        rval[4] = np.dot([x1, y2], r)
        return rval
    
    def polygon_area(self, coords):
        """
        Calculate area of polygon given list of coordinates. Assuming coords are in UTM unit.
        Source: https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
        """
        # get x and y in vectors
        x = [point[0] for point in coords]
        y = [point[1] for point in coords]
        # shift coordinates
        x_ = x - np.mean(x)
        y_ = y - np.mean(y)
        # calculate area
        correction = x_[-1] * y_[0] - y_[-1] * x_[0]
        main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
        final_area = 0.5 * np.abs(main_area + correction)
        return final_area
        
    def extract_overlap_polygon(self, poly1, poly2):
        """Extract overlap polygon vertices"""
        poly1_geom = self.wkt_vertices(poly1)
        poly2_geom = self.wkt_vertices(poly2)
        # extract overlap polygon
        overlap_nodes = []
        # find polygon-1 nodes inside polygon-2
        for point in poly1_geom:
            output = self.ray_tracing_method(point, poly2_geom)
            if output == True:
                overlap_nodes.append(point)
        # find polygon-2 nodes inside polygon-1
        for point in poly2_geom:
            output = self.ray_tracing_method(point, poly1_geom)
            if output == True:
                overlap_nodes.append(point)
        # find intersection nodes
        line_segment_poly1 = [[poly1_geom[j], poly1_geom[j+1]] for j in range(len(poly1_geom)-1)]
        line_segment_poly2 = [[poly2_geom[j], poly2_geom[j+1]] for j in range(len(poly2_geom)-1)]
        # loop over list of nodes
        for line1 in line_segment_poly1:
            for line2 in line_segment_poly2:
                point = self.line_intersection(line1, line2)
                if point != None:
                    overlap_nodes.append(point)
        # create final polygon node list from list of nodes
        overlap_nodes_unique = list(map(list, set(map(tuple, overlap_nodes))))
        # sort list of nodes
        nodes = self.sort_counter_clockwise(overlap_nodes_unique)
        # append first node to create close polygon
        poly_overlap_nodes = nodes + [nodes[0]]
        return poly_overlap_nodes
