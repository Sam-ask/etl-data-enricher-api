import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Eliminar filas que estén completamente vacías
    df_cleaned = df.dropna(how='all')
    
    # 2. Eliminar filas duplicadas (si alguien se registró dos veces igual)
    df_cleaned = df_cleaned.drop_duplicates()
    
    # 3. Quitar espacios en blanco al inicio y al final de los textos
    # (Ejemplo: corrige " Juan " para que sea "Juan")
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        
    return df_cleaned