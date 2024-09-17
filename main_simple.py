#%% Import in the relevant libraries
#===================================
from fastapi import FastAPI         # Create the API for our end user(s)
from fastapi import HTTPException   # Set own HTTP error calls 
from enum import Enum
from pydantic import BaseModel, Field      # Data Validation
from fastapi import Cookie, Header              #for cookie settings
import uvicorn


#%% Set the Model instance and needed attributes
#==================================
class MLModel(str, Enum):
    linreg = "linreg"
    logreg = "logreg"
    xgboost = "xgboost"

#%% file path for text file to see in API
#=================================
file_path = "example.txt"

# list of dicts to return input?
#=================================
fake_items_db = [{"item_name": "Foo"}, {"item_name" : "Bar"}, {"item_name": "Baz"}]

class DBItem (BaseModel):
    item_name : str

#%% Create the API
#==================================
app = FastAPI()

# main landing page ? the first thing that lands, cant be used more than once as the first one is always used 
#---------------------------------
@app.get("/")
async def root():
    return {"message": "Hello there! Welcome to my simple example of an API created 😊"}

# say that a item is needed to continue with instructions
#----------------------------------
@app.get("/items")
async def get_item():
    return {"Please add /item_id (number) to the url please "}

# used when items with an number is specified
#----------------------------------
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id != 27:
        return {"item_id": item_id}
    else:
        return["we hit the jackpot folks! YAAAAYYY!"]
    

# return some names when /users is added to url
#---------------------------------
@app.get("/users")
async def get_users():
    return ["lulu", "louis"]

# bring back values based on MLModel name input from user in url
#---------------------------------
@app.get("/models")
async def get_model():
    return {"Please add /model (linreg, logreg, xgboost) to the url please"}

@app.get("/models/{model_name}")
async def get_model(model_name: MLModel):
    if model_name == MLModel.linreg:
        return {"model_name":model_name, "message":MLModel.linreg}
    elif model_name.value == "logreg":
        return {"model_name": model_name, "message": "Lets do some Logistic Regression!"}
    elif model_name == MLModel.xgboost:
        return {"model_name": model_name, "message": "Lets prune many trees in XGBoost!"}
    

# to determine a file path? not overly support by fastAPI but by starltte in the backend
# --------------------------------- 
@app.get("/files")
async def get_file():
    return{"please provide the filepath"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path":file_path}


# to return iitems from fake db?
#----------------------------------
@app.get("/db/")
async def read_db(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
'''http://127.0.0.1:8000/db/?skip=1&limit=10'''

# Add itme in fake db?
#----------------------------------
@app.put("/db/")
async def add_db_entry(db_entry:DBItem):
    return {"DBItem":DBItem}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)