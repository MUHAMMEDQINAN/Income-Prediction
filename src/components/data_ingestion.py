from dataclasses import dataclass
import os,sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation
from src.logger import logging
from src.exception import CustomException


# Create configuration class to store file path for train test and raw data
@dataclass
# @dataclass: Automatically creates an initializer (__init__) for the class.
class DataIngestionConfig:
    train_data_path = os.path.join("artifacts/data_ingestion","train.csv")
    test_data_path = os.path.join("artifacts/data_ingestion","test.csv")
    raw_data_path = os.path.join("artifacts/data_ingestion","raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    # Implement initiate_data_ingestion method
    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        try:
            logging.info("Reading data")
            data =  pd.read_csv(os.path.join("notebook/data","data.csv"))
            logging.info("Data read successfully")

            # saving the raw data
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)

            # data splitting into training and testing data set
            train_set,test_set = train_test_split(data, test_size = 0.20, random_state = 42)

            # saving the training data
            train_set.to_csv(self.ingestion_config.train_data_path,index = False, header = True)

            # saving the testing data
            test_set.to_csv(self.ingestion_config.test_data_path,index = False,header = True)

            # return the train and test data path
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info("Error occured while data ingestion")

            raise CustomException(e, sys)

    

if __name__ == "__main__":
    obj = DataIngestion()
    train_data_path,test_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data_path,test_data_path)