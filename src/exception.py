from src.logger import logging
import sys


def error_message_detailed(error,error_detailed: sys):
    # error : actual exception that occured (e.g., ZeroDivisionError, FileNotFoundError).
    # error_detailed : used to get detailed traceback information about where the error occurred.
    
    _,_,exc_tb = error_detailed.exc_info()
    # error_detailed.exc_info() extracts the traceback object for the exception.
    # exc_tb: Stores information about where the error occurred.

    # extract the file name where error occured
    file_name = exc_tb.tb_frame.f_code.co_filename

    # create a detailed error message
    error_message = f"Error occured in {file_name} at {exc_tb.tb_lineno} Error Message : {str(error)}"
    
    return error_message

# Defines a custom exception class that extends Python’s built-in Exception class.
class CustomException(Exception):
    def __init__(self,error_message,error_detailed:sys):
        # Calls the parent class (Exception) constructor.
        super().__init__(error_message)
        
        self.error_message = error_message_detailed(error_message,error_detailed=error_detailed)

    def __str__(self):
        return self.error_message



## To check if exception is working
# if __name__ == "__main__":
#     try:
#         a = 1 / 0
#     except Exception as e:
#         logging.info("Division by Zero error")
#         raise CustomException(e,sys)

