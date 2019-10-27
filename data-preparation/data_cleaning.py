import pandas as pd
from pandas.io.json import json_normalize

def clean_status(status_column):
    if(status_column == 'Active'):
        return True
    return False

def clean_use_status(use_status_column):
    if(use_status_column == 'Nuevo'):
        return True
    return False

def clean_data(dataframe):
    clean_status(dataframe['status'])
    clean_use_status(dataframe('use'))