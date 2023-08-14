# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 2016

@author: Debabrata Ghorai, Ph.D.

Digital Number to Radiance Conversion.
"""

import numpy
from osgeo import gdal, gdal_array


def dn_to_radiance(input_image, output_folder, LMAX, LMIN, QCALMIN, QCALMAX, prefix="band"):
    """
    Digital Number to Radiance Conversion.
    References:
    (1) http://osgeo-org.1560.x6.nabble.com/satellite-image-processing-in-Python-td3753422.html
    (2) http://lists.osgeo.org/pipermail/gdal-dev/2012-November/034549.html
    (3) http://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
    (4) http://gis.stackexchange.com/questions/76919/is-it-possible-to-open-rasters-as-array-in-numpy-without-using-another-library
    (5) http://scipy-lectures.github.io/advanced/image_processing/
    """
    # set output file projection from input file
    fopen = gdal.Open(input_image)
    geotransform = fopen.GetGeoTransform()
    prj = fopen.GetProjection()

    # get total input raster bands (count)
    inrasband = [band+1 for band in range(fopen.RasterCount)]

    # set output file driver
    # HFA for *.img reading and writting
    outdriver = gdal.GetDriverByName('GTiff')

    # processing
    for i in inrasband:
        dnfile = fopen.GetRasterBand(i)
        dn = numpy.array(dnfile.ReadAsArray())
        radiance = ((LMAX[i-1] - LMIN[i-1])/(QCALMAX - QCALMIN))*dn + LMIN[i-1]
        # create output file with projection
        radresult = gdal_array.OpenArray(radiance)
        geo = radresult.SetGeoTransform(geotransform)
        proj = radresult.SetProjection(prj)
        # print ("Digital number to radiance conversion for band : %d" % i)
        outputs = outdriver.CreateCopy(
            output_folder+"\\"+prefix+"_"+str(i)+".img", radresult)
    return


# if __name__ == "__main__":
#     input_image = r"E:\Test\sample_landsat5_image.tif"
#     output_folder = r"E:\Test"
#     LMAX = [193.0, 365.0, 264.0, 221.0, 30.2, 16.5]
#     LMIN = [-1.520, -2.840, -1.170, -1.510, -0.370, -0.150]
#     QCALMIN = 1
#     QCALMAX = 255
#     dn_to_radiance(input_image, output_folder, LMAX, LMIN, QCALMIN, QCALMAX)
