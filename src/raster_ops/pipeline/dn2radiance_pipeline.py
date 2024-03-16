from logger import logger
from raster_ops.config import ConfigManager
from raster_ops.components.dn_to_radiance import dn_to_radiance


STAGE_NAME = "Convert DN to Radiance of Satellite image bands"


class DNToRadiancePipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        rstconfig = config.get_rasterdata_config()
        dn_to_radiance(
            rstconfig.raster_infile,
            rstconfig.output_folder,
            rstconfig.lmax_list,
            rstconfig.lmin_list,
            rstconfig.qcal_min,
            rstconfig.qcal_max,
            prefix=rstconfig.prefix
        )
        return


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = DNToRadiancePipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
