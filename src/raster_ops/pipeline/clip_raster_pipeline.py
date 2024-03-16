from osgeo import gdal
from logger import logger
from raster_ops.config import ConfigManager
from raster_ops.components.clip_raster import ClipRaster
from utils import write_geotiff_file, np2gdal_dtype


STAGE_NAME = "Clip raster by clip boundary extent"


class ClipRasterPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        rstconfig = config.get_rasterdata_config()
        obj = ClipRaster(rstconfig=rstconfig)
        clip = obj.subset_by_extent()
        # save raster
        ds = gdal.Open(rstconfig.raster_infile, gdal.GA_ReadOnly)
        src_geotransform = ds.GetGeoTransform()
        src_projection = ds.GetProjectionRef()
        ds = None
        write_geotiff_file(
            clip,
            gt=src_geotransform,
            sr=src_projection,
            outfile_path=rstconfig.clip_raster_file,
            dtype=np2gdal_dtype(str(clip.dtype))
        )
        return


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = ClipRasterPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
