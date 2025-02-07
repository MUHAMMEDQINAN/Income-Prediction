from flask import Flask
from src.logger import logging
from src.exception import CustomException
import sys

#  Initializing the Flask Application
app = Flask(__name__)

#  Defining a Route (Homepage)
@app.route('/',methods = ['GET','POST'])
def index():
    # Handling Errors with try-except
    try:
        raise Exception("we are testing our custom file")
    except Exception as e:
        abc = CustomException(e,sys)
        logging.info(abc.error_message)
        return "Welcome to my ML project on Income Prediction"

# 5️⃣ Running the Flask Application
if __name__ =="__main__":
    app.run(debug=True)