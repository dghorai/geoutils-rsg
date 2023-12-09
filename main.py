from src.logger import logger
from src.exception import error_handling
from src.vector.pipeline.create_grid_pipeline import CreateGridPipeline
from src.vector.pipeline.drainage_area_pipeline import DrainageAreaCalcPipeline
from src.vector.pipeline.merge_vectorfile_pipeline import MergeVectorFilesPipeline
from src.vector.pipeline.nearest_point_pipeline import FindNearestPointPipeline
from src.vector.pipeline.xscl_pipeline import XSCLPipeline

# Select a task number from STAGE_NAME_DICT
task_id = 1

logger.info("Logger import successfull!")

STAGE_NAME_DICT = {
    1: "Generate Grid Polygon of a Point File",
    2: "Drainage Area Calculation",
    3: "Merge Vector Files",
    4: "Find Nearest Point between a Single Point and Line Network",
    5: "Generate Cross-Section Cut-Line of a Line"
}


@error_handling
def switch_case(STAGE_ID, STAGE_NAME):
    match STAGE_ID:
        case 1:
            try:
                logger.info(f">>>>> {STAGE_NAME} started <<<<<")
                obj = CreateGridPipeline()
                obj.main()
                logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
            except Exception as e:
                logger.exception(e)
                raise e

        case 2:
            try:
                logger.info(f">>>>> {STAGE_NAME} started <<<<<")
                obj = DrainageAreaCalcPipeline()
                obj.main()
                logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
            except Exception as e:
                logger.exception(e)
                raise e

        case 3:
            try:
                logger.info(f">>>>> {STAGE_NAME} started <<<<<")
                obj = MergeVectorFilesPipeline()
                obj.main()
                logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
            except Exception as e:
                logger.exception(e)
                raise e

        case 4:
            try:
                logger.info(f">>>>> {STAGE_NAME} started <<<<<")
                obj = FindNearestPointPipeline()
                obj.main()
                logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
            except Exception as e:
                logger.exception(e)
                raise e

        case 5:
            try:
                logger.info(f">>>>> {STAGE_NAME} started <<<<<")
                obj = XSCLPipeline()
                obj.main()
                logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n")
            except Exception as e:
                logger.exception(e)
                raise e


if __name__ == '__main__':
    task_ids = list(STAGE_NAME_DICT.keys())
    if task_id in task_ids:
        # get task_name
        task_name = STAGE_NAME_DICT[task_id]
        # check task_name is string or dictionary
        if isinstance(task_name, str):
            switch_case(task_id, task_name)
        else:
            for task_no in task_name.keys():
                stage_name = task_name[task_no]
                switch_case(task_no, stage_name)
