import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.dropna(how='all')
    
    df_cleaned = df_cleaned.drop_duplicates()
    
   
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        
    return df_cleaned