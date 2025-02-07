# Handling missing values
# Outlier treatment
# Handle Imbalanced data set
# convert categorical column to numerical

import os,sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.logger import logging
from src.exception import CustomException
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from dataclasses import dataclass

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocess_obj_file_path = os.path.join("artifacts/data_transformation","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_obj(self):
        try:
            logging.info("Data Transformation started")

            numerical_features =  ['age', 'workclass',  'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain','capital_loss', 'hours_per_week', 'native_country']

            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            preprocessor= ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_features)
            ])

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        

    def remove_outliers_IQR(self,col,df):
        try:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            upper_limit = Q3 + 1.5 * IQR
            lower_limit = Q1 - 1.5 * IQR

            df[col] = df[col].astype(float)  # Ensure column is float before assignment
            df.loc[(df[col]>upper_limit), col] = upper_limit
            df.loc[(df[col]<lower_limit), col] = lower_limit    

            return df

        except Exception as e:
            raise CustomException(e,sys)
        
    
    # 1️⃣ Call initiate_data_transformation(train_path, test_path)
    # This function is the entry point that starts the data transformation process.
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            # It loads the train and test datasets into Pandas DataFrames.
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            # 2️⃣ Apply Outlier Removal (remove_outliers_IQR)
            # This function is applied to numerical columns to remove  (outliers).and ensure data is clean before transformation

            numerical_features = ['age', 'workclass',  'education_num', 'marital_status','occupation', 'relationship', 'race', 'sex', 'capital_gain','capital_loss', 'hours_per_week', 'native_country']
            for col in numerical_features:
                self.remove_outliers_IQR(col = col,df = train_data)
            logging.info("Outliers capped in our training data")

            for col in numerical_features:
                self.remove_outliers_IQR(col=col,df= test_data)
            logging.info("Outliers capped in our test data")

            # 3️⃣ Create Preprocessing Pipeline (get_data_transformation_obj)
            # This function defines the transformation steps using SimpleImputer and StandardScaler and return ColumnTransformer to apply transformations to numerical features.



            preprocess_obj = self.get_data_transformation_obj()


            # 4️⃣ Split the train  and test data into input and target

            target_column  = "income"
            drop_column = [target_column]

            logging.info("Splitting the train data into dependanat and independant features")
            input_feature_train_data = train_data.drop(drop_column,axis=1)
            target_feature_train_data = train_data[target_column]

            logging.info("Splitting the test data into dependanat and independant features")
            input_feature_test_data = test_data.drop(drop_column,axis=1)
            target_feature_test_data = test_data[target_column]

            # 5️⃣ Fit & Transform Training Data (fit_transform)

            input_train_arr = preprocess_obj.fit_transform(input_feature_train_data)

            # 6️⃣ Transform Test Data (transform)

            input_test_arr = preprocess_obj.transform(input_feature_test_data)

            # 7️⃣ Combine the input and target of transformed arrays

            train_array = np.c_[input_train_arr,np.array(target_feature_train_data)]
            test_array = np.c_[input_test_arr,np.array(target_feature_test_data)]

            # 8️⃣ Save the fitted preprocessing pipeline  and return transformed train and test array

            save_object(file_path = self.data_transformation_config.preprocess_obj_file_path,obj = preprocess_obj)

            return(
                train_array,
                test_array,
                self.data_transformation_config.preprocess_obj_file_path
                
            )

            

        except Exception as e:
            raise CustomException(e,sys)
