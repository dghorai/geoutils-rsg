from src.logger import logger
from src.vector.config import ConfigManager
from src.vector.components.point_to_square_polygon import CreateGrid


STAGE_NAME = "Generate Grid Polygon of a Point File"


class CreateGridPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        pntconfig = config.get_point_config()
        pgconfig = config.get_polygon_config()
        obj = CreateGrid(pntconfig=pntconfig, pgconfig=pgconfig)
        obj.point_to_grid()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = CreateGridPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
