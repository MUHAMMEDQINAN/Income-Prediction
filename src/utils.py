from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from src.logger import logging
from src.exception import CustomException
import os,sys
import pickle

def save_object(file_path,obj):
    # file_path: The location where the object should be saved
    # obj: The object to be saved (e.g., a machine learning model or preprocessing pipeline).
    try:
        # Extract the directory path from file_path
        dir_path =os.path.dirname(file_path)

        # Create the directory (dir_path) if it doesn’t already exist.
        os.makedirs(dir_path,exist_ok=True)

        # Open the file in write-binary mode ("wb") to store the object
        with open(file_path,"wb") as file_obj:
            
            # pickle.dump(obj, file_obj) serializes (converts) the object into a binary format and saves it to file_path.
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def evaluate_model(X_train,y_train,X_test,y_test,model,params):
    try:
        # Empty dictionary to store the accuracy of each trained model
        report = {}

        # for each model in dictionary model and its corresponding hyperparameter is extracted
        # Iterate over model dictionary correctly
        for model_name, model_instance in model.items():
            para = params[model_name]  
            
            # Find the best hyperparameter for each model
            GS = GridSearchCV(model_instance,para,cv = 5)
            GS.fit(X_train,y_train)

            # update the model with the best parameter and train the model again on entire training set
            model_instance.set_params(**GS.best_params_)
            model_instance.fit(X_train,y_train)

            # use each trained model to make prediction and evaluate model perfomance
            y_pred = model_instance.predict(X_test)
            test_model_accuracy = accuracy_score(y_test,y_pred)

            # store each model with correspnding accuarcy score and return the dictionary
            report[model_name] = test_model_accuracy

            return report
        
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path,"rb")  as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e ,sys)