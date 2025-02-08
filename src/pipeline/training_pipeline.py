from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger  import logging

if __name__ == "__main__":  
    logging.info("training pipeline ....")
    obj = DataIngestion()
    train_data_path,test_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr,test_arr,_= data_transformation.initiate_data_transformation(train_data_path,test_data_path)

    model_training = ModelTrainer()
    model_training.initiate_model_trainer(train_arr,test_arr)
