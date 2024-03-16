from logger import logger
from raster_ops.config import ConfigManager
from raster_ops.components.export_land_class import extract_lulc_class


STAGE_NAME = "Export LULC individual class"


class ExportLULCClassPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        rstconfig = config.get_rasterdata_config()
        extract_lulc_class(
            rstconfig.lulc_raster_file,
            rstconfig.lulc_out_raster_file,
            class_number=rstconfig.lilc_class_code
        )
        return


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = ExportLULCClassPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
