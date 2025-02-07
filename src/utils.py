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
