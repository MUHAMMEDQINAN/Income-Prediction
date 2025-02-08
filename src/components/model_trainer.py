import os, sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.utils import save_object
from src.utils import evaluate_model
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# configuration for saving the trained model
@dataclass
class ModelTrainerConfig:
    train_model_file_path = os.path.join("artifacts/model_trainer","model.pkl")

# class responsible for training the model and saving the best one
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Model training started")
            # split data set
            logging.info("splitting our data into dependant and independant features")
            X_train,y_train,X_test,y_test =(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            # defines model and hyperparameter
            model ={
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Logastic": LogisticRegression()                
            }
            params = {
                "Random Forest":{
                    "class_weight":["balanced"],
                    'n_estimators': [20, 50, 30],
                    'max_depth': [10, 8, 5],
                    'min_samples_split': [2, 5, 10],
                },
                "Decision Tree":{
                    "class_weight":["balanced"],
                    "criterion":['gini',"entropy","log_loss"],
                    "splitter":['best','random'],
                    "max_depth":[3,4,5,6],
                    "min_samples_split":[2,3,4,5],
                    "min_samples_leaf":[1,2,3],
                    "max_features":["auto","sqrt","log2"]
                },
                "Logastic":{
                    "class_weight":["balanced"],
                    'penalty': ['l1', 'l2'],
                    'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'solver': ['liblinear', 'saga']
                }          
            }

            # evaluate model return trained model with corresponding accuracy as a dictionary
            model_report = evaluate_model(X_train = X_train,y_train = y_train,X_test  = X_test,y_test =y_test,model = model,params = params)

            # select the best accuracy score(here find the key in model_report with the highest value)
            best_model_score = max(model_report.values())

            # select the best model name
            best_model_name = max(model_report, key=model_report.get)

            best_model =model[best_model_name]
            print(f"Best Model Found, Model Name is: {best_model_name},Accuracy_Score: {best_model_score}")
            print("\n***************************************************************************************\n")
            logging.info(f"best model found, Model Name is {best_model_name}, accuracy Score: {best_model_score}")

            save_object(file_path=self.model_trainer_config.train_model_file_path,obj = best_model)
                        

        except Exception as e:
            raise CustomException(e,sys)