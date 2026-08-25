import pandas as pd
import requests

def enrich_with_ip(df: pd.DataFrame) -> pd.DataFrame:
    if 'IP' not in df.columns:
        return df
    
    ciudades = []
    paises = []
    
    for ip in df['IP']:
        if pd.isna(ip) or str(ip).strip() == "":
            ciudades.append("Desconocido")
            paises.append("Desconocido")
            continue
        
        try:
            url = f"https://ipinfo.io/{ip}/json"
            respuesta = requests.get(url, timeout=5)
            
            if respuesta.status_code == 200:
                datos = respuesta.json()
                ciudades.append(datos.get("city", "Desconocido"))
                paises.append(datos.get("country", "Desconocido"))
            else:
                ciudades.append("Error de API")
                paises.append("Error de API")
        except:
            ciudades.append("Fallo de conexión")
            paises.append("Fallo de conexión")
            
    df['Ciudad'] = ciudades
    df['País'] = paises
    
    return df