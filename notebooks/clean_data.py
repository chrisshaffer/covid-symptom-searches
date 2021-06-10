import pandas as pd

def clean_data(searches,hospitalizations):
        
    df = pd.merge(searches,hospitalizations, how='outer', on = ['key','date'])
    # df.fillna(0,inplace=True)
    
    return df