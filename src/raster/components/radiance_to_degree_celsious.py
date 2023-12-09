# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 2016

@author: Debabrata Ghorai, Ph.D.

Radiance to degree celsious conversion.
"""

import numpy
from osgeo import gdal, gdal_array


def radiance_to_degreecelsious(radiance_image, output_folder, prefix="atmradi_band"):
    # set output file projection from input file
    fopen = gdal.Open(radiance_image)
    geotransform = fopen.GetGeoTransform()
    prj = fopen.GetProjection()

    # get total input raster bands (count)
    inrasband = [band+1 for band in range(fopen.RasterCount)]

    # degree Celsiuos conversion parameters
    k2 = 1260.56  # degrees Kelvin constant for LT5-TM
    k1 = 607.76  # degrees Kelvin constant for LT5-TM

    # set output file driver
    # HFA for *.img reading and writting
    outdriver = gdal.GetDriverByName('HFA')

    # processing
    for i in inrasband:
        atmradfile = fopen.GetRasterBand(i)
        atmradi = numpy.array(atmradfile.ReadAsArray())
        var1 = (k1/atmradi)
        var2 = numpy.log(var1+1)
        degreeKelvin = (k2/var2)
        degreeCelsious = degreeKelvin - 273.0
        # create output file with projection
        dcresult = gdal_array.OpenArray(degreeCelsious)
        geo = dcresult.SetGeoTransform(geotransform)
        proj = dcresult.SetProjection(prj)
        # print("Temperature in degree Celsious for band : %d" % i)
        outputs = outdriver.CreateCopy(
            output_folder+"\\"+prefix+"_"+str(i)+".img", dcresult)
    return


# if __name__ == "__main__":
#     radiance_image = r"E:\PythonProgramming\sample_radiance_image.img"
#     output_folder = r"E:\PythonProgramming\output_temperature_image"
#     radiance_to_degreecelsious(radiance_image, output_folder)
