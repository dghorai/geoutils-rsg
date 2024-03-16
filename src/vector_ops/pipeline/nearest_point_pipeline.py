from logger import logger
from vector_ops.config import ConfigManager
from vector_ops.components.find_nearest_point import FindNearestPoint


STAGE_NAME = "Find Nearest Point between a Single Point and Line Network"


class FindNearestPointPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        pntconfig = config.get_point_config()
        plineconfig = config.get_polyline_config()
        obj = FindNearestPoint(pntconfig=pntconfig, plineconfig=plineconfig)
        obj.find_closest_point()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = FindNearestPointPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
