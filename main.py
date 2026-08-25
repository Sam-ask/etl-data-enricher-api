from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from openpyxl.styles import PatternFill, Font
import pandas as pd
import io

# Importamos a nuestros dos trabajadores
from services.data_cleaner import clean_data
from services.ip_enricher import enrich_with_ip

# 1. Creamos la aplicación con sus metadatos
app = FastAPI(
    title="Data Enricher ETL",
    description="API para limpieza de datos y enriquecimiento geográfico",
    version="1.0.0"
)

# 2. Configuramos la ruta con descripciones en español para la documentación
@app.post(
    "/upload", 
    summary="Procesar archivo de datos (ETL)", 
    description="Sube un archivo Excel (.xlsx) o CSV. El sistema lo limpiará, eliminará basura y buscará la ubicación de las IPs.",
    tags=["Módulo de Procesamiento"]
)
async def upload_file(file: UploadFile = File(..., description="Selecciona tu archivo Excel o CSV")):
    # Validamos que solo acepten Excel o CSV
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Formato no soportado. Usa .csv o .xlsx")
    
    try:
        contents = await file.read()
        
        # PASO 1: Extraer (Leer el archivo crudo)
        if file.filename.endswith('.csv'):
            df_crudo = pd.read_csv(io.BytesIO(contents))
        else:
            df_crudo = pd.read_excel(io.BytesIO(contents))
            
        # PASO 2: Transformar (Limpiar la basura)
        df_limpio = clean_data(df_crudo)
        
        # PASO 3: Enriquecer (Buscar las ubicaciones de las IP)
        df_final = enrich_with_ip(df_limpio)
            
        # PASO 4: Cargar y dar ESTILO (Crear el nuevo Excel en memoria)
        buffer_salida = io.BytesIO()
        
        # Usamos openpyxl como motor para poder "pintar" el Excel
        with pd.ExcelWriter(buffer_salida, engine='openpyxl') as writer:
            df_final.to_excel(writer, index=False, sheet_name='Datos_Procesados')
            
            # Accedemos a la hoja de trabajo para darle estilo
            worksheet = writer.sheets['Datos_Procesados']
            
            # Configuramos el color (Teal corporativo) y letra blanca en negritas
            color_fondo = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")
            fuente_blanca = Font(bold=True, color="FFFFFF")
            
            for col in worksheet.columns:
                # Ajustar el ancho de las columnas automáticamente
                longitud_maxima = max(len(str(celda.value)) for celda in col if celda.value)
                letra_columna = col[0].column_letter
                worksheet.column_dimensions[letra_columna].width = longitud_maxima + 2
                
                # Pintar la primera fila (Cabeceras)
                celda_cabecera = col[0]
                celda_cabecera.fill = color_fondo
                celda_cabecera.font = fuente_blanca

        # Regresamos el "cassette" al inicio para que se pueda descargar
        buffer_salida.seek(0)
        
        # Configuramos los encabezados de internet para forzar la descarga del archivo
        headers = {
            'Content-Disposition': f'attachment; filename="Procesado_{file.filename}"'
        }
        
        # ¡Devolvemos el archivo físico listo para descargar!
        return StreamingResponse(
            buffer_salida, 
            headers=headers, 
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")