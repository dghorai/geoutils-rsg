# %%
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Merge vector files.
"""

# %%
import os

from osgeo import ogr

# %%
def find_file_geomtype(geom_type=''):
    if geom_type == 'Point':
        geometryType = ogr.wkbPoint
    elif geom_type == 'Line':
        geometryType = ogr.wkbLineString
    elif geom_type == 'Polygon':
        geometryType = ogr.wkbPolygon
    else:
        geometryType = None
    return geometryType

# %%
def merge_vector_files(outfile, filedir, geom_type=None):
    # get list of vector files
    fileList = os.listdir(filedir)
    # get spatial reference from first file
    infc = [filedir+'/'+f for f in fileList if f.endswith('.shp')][0]
    shapefile = ogr.Open(infc)
    layer = shapefile.GetLayer(0)
    srs = layer.GetSpatialRef()
    srs.ExportToWkt()
    # get driver
    out_driver = ogr.GetDriverByName('ESRI Shapefile')
    geometryType = find_file_geomtype(geom_type=geom_type)
    if os.path.exists(outfile):
        out_driver.DeleteDataSource(outfile)
        out_ds = out_driver.CreateDataSource(outfile)
        out_layer = out_ds.CreateLayer("lyr_outfile", srs, geom_type=geometryType)
    else:
        out_ds = out_driver.CreateDataSource(outfile)
        out_layer = out_ds.CreateLayer("lyr_outfile", srs, geom_type=geometryType)
    # loop over vector files and merge them
    for f in fileList:
        if f.endswith('.shp'):
            ds = ogr.Open(filedir+"/"+f)
            lyr = ds.GetLayer()
            if lyr.GetGeomType() == geometryType:
                for feat in lyr:
                    out_feat = ogr.Feature(out_layer.GetLayerDefn())
                    out_feat.SetGeometry(feat.GetGeometryRef().Clone())
                    out_layer.CreateFeature(out_feat)
                    out_layer.SyncToDisk()
            else:
                pass
            ds = None
    return "Process Completed!"

# %%
if __name__ == "__main__":
    filedir = r"D:\Coding\vscode_project\rsgis-scripts\test\sample_data"
    outfile = r"D:\Coding\vscode_project\rsgis-scripts\test\sample_data\merge_lines.shp"
    merge_vector_files(outfile, filedir, geom_type='Line')



