from logger import logger
from vector.config import ConfigManager
from vector.components.merge_vector_files import MergeVectorFiles


STAGE_NAME = "Merge Vector Files"


class MergeVectorFilesPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigManager()
        vdconfig = config.get_vectordata_config()
        obj = MergeVectorFiles(vdconfig=vdconfig)
        obj.merge_vector_files()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        obj = MergeVectorFilesPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
    except Exception as e:
        logger.exception(e)
        raise e
