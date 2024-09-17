#%% Import in the relevant libraries
#===================================
from fastapi import FastAPI         # Create the API for our end user(s)
from fastapi import HTTPException   # Set own HTTP error calls 

#%% Create the API
#==================================
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello there! Welcome to my simple example of an API created 😊"}