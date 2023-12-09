# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Extract pixel value at given point from raster data.
"""

import struct

from osgeo import gdal, gdalconst


def raster_to_array(rasterfile):
    imgDataSource = gdal.Open(rasterfile, gdalconst.GA_ReadOnly)
    geoTransform = imgDataSource.GetGeoTransform()
    rasterBands = imgDataSource.GetRasterBand()
    return rasterBands, geoTransform


def extract_pixel_value(imgfile, point_list):
    """
    Extract pixel value at given point.
    Reference: http://gis.stackexchange.com/questions/46893/how-do-i-get-the-pixel-value-of-a-gdal-raster-under-an-ogr-point-without-numpy
    """

    # get raster array
    rasterBands, geoTransform = raster_to_array(imgfile)

    pnt_values = []
    for point in point_list:
        # get x and y from point
        mx, my = point  # Coordinates in map units

        # extract value
        px = int((mx - geoTransform[0])/geoTransform[1])  # X pixel
        py = int((my - geoTransform[3])/geoTransform[5])  # Y pixel

        # Assumes 16 bit int aka 'short'
        structVal = rasterBands.ReadRaster(
            px, py, 1, 1, buf_type=gdal.GDT_UInt16)

        # Use the 'short' format code (2 bytes) not int (4 bytes)
        intVal = struct.unpack('h', structVal)

        # print(intVal[0]) # intVal is a tuple, length=1 as we only asked for 1 pixel value
        pnt_values.append([mx, my, intVal[0]])

    return pnt_values


# if __name__ == "__main__":
#     sample_point = [[84.4874, 18.8998]]
#     imgfile = r"E:\PhD_Working\DataSets\sample_image.tif"
#     pixvalue = extract_pixel_value(imgfile, sample_point)
