from logger import logger
from raster_ops.components.convert_raster_to_point import raster_to_point
from raster_ops.config import ConfigManager


STAGE_NAME = "Convert gray-scale raster to point shapefile"


class RasterToPointPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        rstconfig = config.get_rasterdata_config()
        raster_to_point(
            rstconfig.raster_infile,
            rstconfig.out_point_file
        )
        return


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = RasterToPointPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
