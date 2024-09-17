''' Code to create a streamlit front end with a Fast Api backend :)'''
#%% import libraries needed
#===================================
import streamlit as st              #webapp UI
import json                         # Json operations
import requests                     # HTTP requests

import uvicorn
import main_simple
import main_duckdb
import main_ml2

from pydantic import BaseModel

#%% Create the app layout 
#==================================
st.title(body= 'Welcome to FastAPI and Streamlit!')

# url where all api stuff is from 
url = 'http://127.0.0.1:8000/'
# Choose the APi to run
api_option = st.selectbox(
                            label=' What api would you like to call from? 🤔'
                          , options= ('Simple', 'DuckDB', 'Machine Learning')
                         )

st.write("")

# Run stuff once the button is pressed 
if st.button(label='Run'):
    if api_option == "Simple":
       main_simple
        
    elif api_option == "DuckDB":
        pass
    elif api_option == 'Machine Learning':
      pass

