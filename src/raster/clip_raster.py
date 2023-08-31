# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 2016

@author: Debabrata Ghorai, Ph.D.

Clip Raster Data.
"""

import sys

from osgeo import gdal, gdalnumeric, ogr
import numpy


class ClipRaster:
    """
    Clip Raster Data.
    Source: http://stackoverflow.com/questions/13416764/clipping-raster-image-with-a-polygon-suggestion-to-resolve-an-error-related-to
    """

    def __init__(self, inRaster, inPolygon):
        """constructure"""
        self.inRaster = inRaster
        self.inPolygon = inPolygon

    def world2Pixel(self, geoMatrix, x, y):
        ulX = geoMatrix[0]
        ulY = geoMatrix[3]
        xDist = geoMatrix[1]
        pixel = numpy.round((x - ulX) / xDist).astype(numpy.int)
        line = numpy.round((ulY - y) / xDist).astype(numpy.int)
        return pixel, line

    def subset_by_extent(self):
        # Open the image as a read only image
        ds = gdal.Open(self.inRaster, gdal.GA_ReadOnly)
        # Check the ds (=dataset) has been successfully open
        # otherwise exit the script with an error message.
        if ds is None:
            raise SystemExit("The raster could not openned")
        # get total input raster bands (count)
        inrasband = [band+1 for band in range(ds.RasterCount)]

        # Get image georeferencing information.
        geoMatrix = ds.GetGeoTransform()
        ulX = geoMatrix[0]
        ulY = geoMatrix[3]
        # open shapefile (= border of are of interest)
        shp = ogr.Open(self.inPolygon)
        if not len(shp) is 1:
            print("The shapefile with more than 1 record")
            sys.exit(-1)
        source_shp = ogr.GetDriverByName("Memory").CopyDataSource(shp, "")
        # Create an OGR layer from a boundary shapefile
        source_layer = source_shp.GetLayer(0)
        # Convert the layer extent to image pixel coordinates
        minX, maxX, minY, maxY = source_layer.GetExtent()
        ulX, ulY = self.world2Pixel(geoMatrix, minX, maxY)
        lrX, lrY = self.world2Pixel(geoMatrix, maxX, minY)
        # Calculate the pixel size of the new image
        # Load the source data as a gdalnumeric array
        srcArray = gdalnumeric.LoadFile(self.inRaster)
        if len(inrasband) > 1:
            clip = srcArray[:, ulY:lrY, ulX:lrX]  # For RGB raster
        else:
            clip = srcArray[ulY:lrY, ulX:lrX]  # For gray scale raster
        return clip
