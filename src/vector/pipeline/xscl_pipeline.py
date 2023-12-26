from logger import logger
from vector.config import ConfigManager
from vector.components.create_crosssection_line import XSCL

STAGE_NAME = "Generate Cross-Section Cut-Line of a Line"


class XSCLPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        plconfig = config.get_polyline_config()
        obj = XSCL(plconfig=plconfig)
        obj.create_xscl_uniqueid()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = XSCLPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
