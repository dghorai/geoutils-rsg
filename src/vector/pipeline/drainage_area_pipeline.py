from src.logger import logger
from src.vector.config import ConfigManager
from src.vector.components.calculate_cumulative_drainage_area import DrainageAreaCalc

STAGE_NAME = "Drainage Area Calculation"


class DrainageAreaCalcPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        plconfig = config.get_polyline_config()
        pgconfig = config.get_polygon_config()
        obj = DrainageAreaCalc(plconfig=plconfig, pgconfig=pgconfig)
        obj.cumulative_drainage_area()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = DrainageAreaCalcPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
