**ETL Data Enricher (Python)**
markdown
# ETL Data Enricher API

Una API RESTful construida con FastAPI y Python que ejecuta un pipeline ETL (Extracción, Transformación y Carga) en memoria. El sistema procesa archivos de datos, limpia registros basura y enriquece la información consumiendo servicios de geolocalización externos.

## Tecnologías Utilizadas
- Framework Backend: FastAPI (Python)
- Procesamiento de Datos: Pandas
- Peticiones HTTP (Consumo de API REST): Requests
- Manipulación de Excel: Openpyxl
- Servidor ASGI: Uvicorn

## Características Principales

1. Extracción (Extract): 
   - Acepta carga de archivos en formatos .csv y .xlsx.
   - Carga de datos directamente en memoria RAM para un procesamiento ultrarrápido sin saturar el disco.
2. Transformación (Transform - Limpieza):
   - Eliminación automática de filas vacías y registros duplicados con Pandas.
   - Estandarización de cadenas de texto (eliminación de espacios en blanco).
3. Enriquecimiento (Enrich):
   - Identificación de direcciones IP en el dataset.
   - Consumo de la API pública de IPinfo para geolocalizar (Ciudad y País) cada IP en tiempo real.
4. Carga y Exportación (Load):
   - Generación de un nuevo archivo Excel (.xlsx) de salida.
   - Aplicación automática de estilos corporativos (colores, negritas) y auto-ajuste de ancho de columnas usando openpyxl.

## Cómo ejecutarlo localmente

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/Sam-ask/etl-data-enricher-api.git](https://github.com/Sam-ask/etl-data-enricher-api.git)
