#%% Import in the relevant libraries
#===================================
from fastapi import FastAPI         # Create the API for our end user(s)
from fastapi import HTTPException   # Set own HTTP error calls 
from pydantic import BaseModel, Field      # Data Validation
from fastapi import Cookie, Header, Response ,Request        #for cookie settings
import uvicorn

import pickle
import pandas as pd

#%% Load in models created in main_ml1.ipynb
#==================================

with open('tree_model.pkl', 'rb') as f:
    tree_model = pickle.load(f)
with open('log_model.pkl', 'rb') as f:
    log_model = pickle.load(f)

with open('xgb_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)

#%% Load in test data to predict against ? 
#==================================
X_test = pd.read_csv('predict_on.csv')
y_test_tree = tree_model.predict_proba(X_test)[:,1]
y_test_log = log_model.predict_proba(X_test)[:,1]


#%% create a class to check a record pulled through
class Features(BaseModel):
      Pclass: int
      Age: int
      Fare: int
      Cabin: int
      Gender: bool
      Family_size: int
      Emb_Southampton: bool
      Emb_Cherbourg: bool
      Emb_Queenstown: bool

#%% Create the API
#==================================
app = FastAPI()

# main landing page ? the first thing that lands, cant be used more than once as the first one is always used 
#---------------------------------
@app.get("/")
async def root():
    return {"message": "Hello there! Welcome to my ml example of an API created 😊"}


@app.get("/survival/predict/")
async def predict():
    return {
            "Decision Tree Probability (Percent) of passenger survival": (y_test_tree[0]*100)
            ,"Logistic Regression Probability (Percent) of passenger survival":(y_test_log[0]*100)
            }

# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8003)
