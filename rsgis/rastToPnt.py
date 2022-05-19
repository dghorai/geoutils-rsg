# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 2016

@author: Debabrata Ghorai, Ph.D.

Convert raster to point shapefile.
"""

from osgeo import gdal, gdalconst, gdalnumeric, ogr, osr


def raster_to_point(raster_data, outpoint_file, outfield="DN"):
    # read raster image
    ds = gdal.Open(raster_data, gdalconst.GA_ReadOnly)
    # GetGeoTransform
    geot = ds.GetGeoTransform()
    geop = ds.GetProjection()
    min_x = geot[0]
    max_y = geot[3]
    max_x = min_x + geot[1]*ds.RasterXSize
    min_y = max_y + geot[5]*ds.RasterYSize
    # get spatial reference from raster image
    sr = osr.SpatialReference()
    sr.ImportFromWkt(ds.GetProjection())
    # create shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapeData = driver.CreateDataSource(outpoint_file)
    # create layer
    lyr = shapeData.CreateLayer('point_layer', sr, ogr.wkbPoint)
    # add field
    lyr.CreateField(ogr.FieldDefn(outfield, ogr.OFTReal))
    # lyr defn
    lyrDef = lyr.GetLayerDefn()
    # dataset to array
    array = gdalnumeric.LoadFile(raster_data)
    # iterate over the numpy points
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            try:
                x = j*geot[1] + min_x + geot[1]/2.0
                y = i*geot[5] + max_y + geot[5]/2.0
                # create points
                point = ogr.Geometry(ogr.wkbPoint)
                point.SetPoint(0, x, y)
                # put point as a geometry inside a feature
                featIndex = 0
                feat = ogr.Feature(lyrDef)
                feat.SetField(outfield, array[i][j])
                feat.SetGeometry(point)
                feat.SetFID(featIndex)
                # put feature in a layer
                lyr.CreateFeature(feat)
            except:
                pass
    # Flush
    shapeData.Destroy()
    return "Process Completed!"


if __name__ == "__main__":
    raster_data = r"G:\MyWorkingFolder\sample_image.img"
    outpoint_file = r"G:\MyWorkingFolder\point_shapefile.shp"
    raster_to_point(raster_data, outpoint_file)