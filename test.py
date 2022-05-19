# import modules
import pandas as pd

import rsgis.lineGeom as pg
from rsgis.wktOps import WktUtils
import rsgis.xsclGeom as gm
import rsgis.merge as mv
import rsgis.nearestPnt as fp
import rsgis.pntToSquarePoly as grd
import rsgis.clipRast as clip

op = WktUtils()



# inputs
infc = r"D:\Coding\vscode\rsgis-scripts\sample_data\sample_drainage_lines.shp"
inwkts = r"D:\Coding\vscode\rsgis-scripts\sample_data\sample_wkts.csv"


# create line object id
pg.CreateObjectID(infc, fieldname="OBJECTID")


# create line-connected group id
pg.CreateGroupID(infc, fieldname="GROUPID")


# generate river line hydroid
pg.GenerateHydroID(infc, groupid="GROUPID", outfield="HYDROID")


# line direction (if direction_errors return empty then no direction error in river line)
direction_errors = pg.LineDirectionError(infc)


# get overlap area
wkt_df = pd.read_csv(inwkts)
poly_overlap_nodes = op.extract_overlap_polygon(wkt_df['WKT'][0], wkt_df['WKT'][1])


# generate perpendicular line at specific interval
outfc = r"D:\Coding\vscode\rsgis-scripts\sample_data\output\out_cross_section.shp"
gm.construct_perpendicular_line(infc, outfc=outfc, interval=1000, offset=250, coordsys='GCS')
gm.create_xscl_uniqueid(xscl_available=True, infc=infc, outfc=outfc, uidfield="UID", interval=1000, offset=250, coordsys='GCS')


# merge vector files
filedir = r"D:\Coding\vscode\rsgis-scripts\sample_data"
outfile = r"D:\Coding\vscode\rsgis-scripts\sample_data\output\merge_lines.shp"
mv.merge_vector_files(outfile, filedir, geom_type='Line')


# get nearest point
point = [84.4874, 18.8998]
nearest_pnt = fp.find_closest_point(point, infc)
print(nearest_pnt)


# point to grid conversion
inpoints = r"D:\Coding\vscode\rsgis-scripts\sample_data\sample_grid_points.shp"
outgrid = r"D:\Coding\vscode\rsgis-scripts\sample_data\output\point_to_grid.shp"
grd.point_to_grid(inpoints, outgrid, offset=5000, coordsys='GCS')


# convert ipynb to py file in vscode: ctrl+shift+p --> type Export --> select Export to Python Script
inRaster = r"D:\Coding\vscode\rsgis-scripts\sample_data\sample_raster_dem.tif"
inPolygon = r"D:\Coding\vscode\rsgis-scripts\sample_data\clip_boundary.shp"
clip_raster = clip.ClipRaster(inRaster, inPolygon)
result_array = clip_raster.subset_by_extent()