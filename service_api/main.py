
import os
import json
import time
import pandas as pd
import requests
from pydantic import BaseModel, validator

from typing import Optional as OptionalType

from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, HTTPException, Request

from starlette.middleware.base import BaseHTTPMiddleware
import logging

import hashlib

from datetime import datetime

#from utils import Configuration
from CyberSource import *
from pathlib import Path
import os
import json
from importlib.machinery import SourceFileLoader
from CyberSource.api.report_downloads_api import ReportDownloadsApi

config_file = os.path.join(os.getcwd(), "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

app = FastAPI(title="Cyber API",
              description="""Obtener datos de Cyber y ponerlos en Storage Izipay""",
              version="0.0.1"
             )


origins = ["*"]

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     IPRestrictionMiddleware,
#     authorized_ips=AUTHORIZED_IPS
# )

class RequestCyberModel(BaseModel):
    organization_id: str
    merchant_key_id: str
    merchant_secret_key_id: str
    report_name: str
    fecha: str = datetime.now().strftime("%Y-%m-%d")

#current_date = datetime.now()
#formatted_date = current_date.strftime("%Y-%m-%d")

# @app.before_request
# def restrict_ip():
#     # Obtén la IP del cliente (usa X-Forwarded-For si estás detrás de un proxy)
#     client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
#     # Verifica si la IP es autorizada
#     if client_ip != AUTHORIZED_IP:
#         return jsonify({"error": "Acceso denegado"}, 403)


def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def download_report(process_date, report_name, organization_id, merchant_id, merchant_secret_id):
    organizationId = organization_id #PARAMETRIZAR
    reportDate = process_date
    reportName = report_name #PARAMETRIZAR

    try:
        config_obj = configuration.Configuration(organization_id=organizationId, merchant_id=merchant_id, merchant_secret_id=merchant_secret_id)

        client_config = config_obj.get_configuration()
        api_instance = ReportDownloadsApi(client_config)
        #api_instance.api_client.download_file_path = os.path.join(os.getcwd(), "resources", "download_report.csv")
        api_instance.api_client.download_file_path = os.path.join(os.getcwd(), csv_path)
        print(f"antes del download report\n {organizationId}, {reportDate}, {reportName}")
        status, headers = api_instance.download_report(reportDate, reportName, organization_id=organizationId)

        print("Download Status : ", status)
        print("Response Headers : ", headers)

        print("Response downloaded at the location : " + api_instance.api_client.download_file_path)
        #write_log_audit(status)
    except Exception as e:
        #write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling ReportDownloadsApi->download_report: %s\n" % e)

def load_cyber_report(csv_path):
    try:
        # Intentar leer el archivo, saltando la primera fila y forzando todo a string
        df = pd.read_csv(csv_path, dtype=str, skiprows=1)

        # Verificar si el DataFrame está vacío o tiene columnas mal formateadas
        if df.empty or any('unnamed' in col.lower() for col in df.columns):
            print("❌ Error en la carga: el archivo está vacío o tiene columnas inválidas ('Unnamed').")
            df_cyber = pd.DataFrame()
        else:
            print("✅ Archivo cargado correctamente.")
            print("Columnas:", df.columns.tolist())
            print("Número de filas:", len(df))
            df_cyber = df

    except Exception as e:
        print(f"❌ Error al intentar leer el archivo: {e}")
        df_cyber = pd.DataFrame()

    return df_cyber

def fn_ingesta(fecha, report_name, var_bucket_name, var_project_id, var_dataset_id, df_cyber):
    from datetime import datetime, timedelta
    import gc
    from google.cloud import storage

    fecha0 = datetime.strptime(fecha, "%Y-%m-%d")
    fecha_d_1 = fecha0 - timedelta(days=1)
    fecha_d_1yyyymmdd = fecha_d_1.strftime("%Y%m%d")

    try:
        df = df_cyber.copy()

        # Eliminar columnas sin cabecera
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.astype(str).replace('nan', None)

        if df.empty or df.isnull().all().all():
            print(f"⚠️ Archivo creado para {fecha}, pero está vacío. No se cargará.")
        else:
            # Guardar en Parquet
            file_name = f"{report_name}_{fecha_d_1yyyymmdd}.parquet"
            df.to_parquet(file_name, index=False)

            # Subir a GCS
            storage_client = storage.Client()
            bucket = storage_client.bucket(var_bucket_name)
            destination_blob_name = f"Cybersource/Transaccional/{report_name}/{fecha_d_1yyyymmdd[:4]}/{fecha_d_1yyyymmdd[4:6]}/{file_name}"
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_name)

            print(f"✅ Archivo '{file_name}' guardado en Cloud Storage en '{destination_blob_name}'")

            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"Excel {file_name} temporal eliminado.")

        del df
        gc.collect()

    except Exception as e:
        print(f"❌ Error durante la ingesta para {fecha}: {e}")

# Home page
@app.get("/")
def home( token: str = Header(None)):
    if token is None or token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"message": "API Cybersource Izipay", "model_version": 0.1}

@app.post("/cyber")
def api_cyber(payload: RequestCyberModel, token: str = Header(None)):

    if token is None or token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Get Data
    data = payload.dict()
    print('Payload:', data)

    #current_date = datetime.now()
    #formatted_date = current_date.strftime("%Y-%m-%d")
    var_bucket_name = BUCKET_NAME
    var_project_id = GCP_PROJECT_ID
    var_dataset_id = ''
    var_file = ''
    var_source =''
    #fecha =  formatted_date

    #data_input = data.get('input')
    fecha = data.get('fecha')
    organization_id = data.get('organization_id')
    merchant_key_id = data.get('merchant_key_id')
    merchant_secret_key_id = data.get('merchant_secret_key_id')
    report_name = data.get('report_name')

    try:
        response = {}

        download_report(fecha, report_name, organization_id, merchant_key_id, merchant_secret_key_id)
        df_cyber = load_cyber_report(csv_path=csv_path)
        fn_ingesta(fecha, report_name, var_bucket_name, var_project_id, var_dataset_id, df_cyber)
        response["success"] = True
        #ruta_archivo = "/ruta/al/archivo.txt"

        if os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"Excel {csv_path} temporal eliminado.")
        return response
    except Exception as e:
        print("error ->  ",str(e))
        raise HTTPException(status_code=401, detail=str(e))

# Startup
async def startup_event():
    global SECRET_TOKEN
    global GCP_PROJECT_ID
    global BUCKET_NAME
    global api_logger
    global csv_path
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', "my-secret-token")
    SECRET_TOKEN = os.getenv('SECRET_TOKEN', "my-secret-token")
    BUCKET_NAME = os.getenv('BUCKET_NAME', "my-secret-token")

    # Crear carpeta si no existe
    resources_path = 'resources'
    os.makedirs(resources_path, exist_ok=True)

    # Crear CSV vacío
    current_date = datetime.now()
    csv_path = os.path.join(resources_path, f'download_report_{current_date}.csv')
    pd.DataFrame().to_csv(csv_path, index=False)

    print(f"Archivo CSV vacío creado en: {csv_path}")

    #api_logger = FirestoreLogs(project_id=GCP_PROJECT_ID, database_id='logs-hushing-ruc',collection_name="collection-logs-hushing-ruc")

    # Inicializar el cliente
    #client = bigquery.Client(project=GCP_PROJECT_ID)

    # cred = credentials.ApplicationDefault()
    # firebase_admin.initialize_app(cred, {'projectId': GCP_PROJECT_ID,})
    # FS_CLIENT = firestore.client()
    print("La aplicación se está iniciando")

app.add_event_handler("startup", startup_event)
