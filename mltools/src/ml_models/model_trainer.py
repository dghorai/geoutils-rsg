import os
import sys

from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor
from logger import logging, CustomException
from utils import save_object, evaluate_model
from config import PRJ_DIR


@dataclass
class ModelTrainerConfig:
    trained_model_filepath = os.path.join(PRJ_DIR, "artifacts", "regression", "random_forest", "model.pkl")


class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, train_arrc, test_arrc):
        try:
            logging.info(
                'Splitting dependent and independent variables from train and test data')

            X_train, y_train, X_test, y_test = (
                train_arrc[:, :-1], train_arrc[:, -1], test_arrc[:, :-1], test_arrc[:, -1])

            # change/add based on model
            models = {
                'RandomForestRegressor': RandomForestRegressor(random_state=0)}

            model_report: dict = evaluate_model(
                X_train, y_train, X_test, y_test, models)

            print(model_report)
            print('\n===========================\n')
            logging.info(f'Model Report: {model_report}')

            # get the best model score and name from dictionary
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(
                model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            print(
                f'Best model found -> Model Name: {best_model_name}, accuracy report: {best_model_score}')
            print('\n===========================\n')
            logging.info(
                f'Best model found -> Model Name: {best_model_name}, accuracy report: {best_model_score}')

            # save model
            save_object(
                file_path=self.model_trainer_config.trained_model_filepath,
                obj=best_model
            )
        except Exception as e:
            logging.info('Exception occured at model training stage')
            raise CustomException(e, sys)
