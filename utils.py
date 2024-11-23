import pandas as pd

def preprocess_data(data):
    # Example: Remove outliers or fill missing values
    data.fillna(0, inplace=True)
    return data
from utils import preprocess_data
data = preprocess_data(data)
