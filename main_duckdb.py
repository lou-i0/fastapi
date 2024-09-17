#%% Import in the relevant libraries
#===================================
from fastapi import FastAPI         # Create the API for our end user(s)
from fastapi import HTTPException   # Set own HTTP error calls 
from enum import Enum
from pydantic import BaseModel, Field      # Data Validation
from fastapi import Cookie, Header, Response         #for cookie settings

import duckdb                        # db application to api
import pandas as pd                  # Pandas dataframes and Analysis


#%% Set up the duckdb database
#==================================
duck = duckdb.connect(database = 'titanic.db')

duck.sql('''
            CREATE OR REPLACE TABLE titanic_passengers AS
            SELECT * FROM read_parquet('tit.parquet') ''')

#%% Declare schema for DB and ensure type setting?
#===================================
class DBSchema(BaseModel):
    Fare : float
    Cabin : int
    Age: float

records = list[DBSchema]

#%% Create the API
#==================================
app = FastAPI()


# main landing page ? the first thing that lands, cant be used more than once as the first one is always used 
#---------------------------------
@app.get("/")
async def root():
    return {"message": "Hello there! Welcome to my duckdb example of an API created 😊"}

# to retrieve data from duckDB SQL query
#--------------------------------
@app.get("/tit_data/")
async def get_tit_data(records = records):
    # if len(records) == 0:
    #     return []
    transaction = duck.begin()

    transaction.execute(query='''
                                CREATE OR REPLACE VIEW titanic_sample AS 
                                SELECT 
                                    Fare
                                    ,Age
                                    ,Cabin
                                FROM 
                                    titanic_passengers
                                LIMIT 10
                              ''')
    result = transaction.query(query = "SELECT * FROM titanic_sample").to_df().to_json(orient='records')
    #result = transaction.query(query='SELECT * FROM titanic_sample').fetchall()

    transaction.rollback()

    return  Response(content=str(result), media_type='application/json')
    #return {"result": result}
    
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)











    