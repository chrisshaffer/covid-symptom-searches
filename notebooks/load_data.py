import pandas as pd

def load_data(dir,nrows,usecols):
        
    # Load data from csv to pd
    hospitalizations = pd.read_csv(dir + 'hospitalizations.csv',nrows=nrows)

    # Columns for searches limited to COVID-19 symptoms
    searches = pd.read_csv(dir + 'google-search-trends.csv',nrows=nrows,usecols=usecols)
    
    # key index
    index = pd.read_csv(dir + 'index.csv')
    
    return hospitalizations, searches, index