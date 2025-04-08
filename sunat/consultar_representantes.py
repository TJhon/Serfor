
import pandas as pd
import sqlite3
import os
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import requests
import random
import string

from representantes_sunat import consultar_ruc
from concurrent.futures import ThreadPoolExecutor

DATA_PATH = './data/raw/infractores_unicos_identificados.csv'
DB_PATH = './data/in/infractores_representantes.db'


def procesar_ruc(ruc, db_path=DB_PATH):
    print(ruc)
    try:
        # Verificar si el RUC ya está en la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS representantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento TEXT,
            nro_documento TEXT,
            nombre TEXT,
            cargo TEXT,
            fecha_desde TEXT,
            ruc TEXT,
            name_empresa TEXT
        )
        ''')
        
        # Verificar si ya existe el RUC en la base de datos
        cursor.execute("SELECT COUNT(*) FROM representantes WHERE ruc = ?", (ruc,))
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            # Ya existe, omitir
            return False, ruc
        
        # Consultar el RUC
        resultado = consultar_ruc(ruc)
        
        if resultado is not None:
            # Renombrar columnas para evitar conflictos
            mapping = {
                'Documento': 'documento',
                'Nro. Documento': 'nro_documento',
                'Nombre': 'nombre',
                'Cargo': 'cargo',
                'Fecha Desde': 'fecha_desde',
                'ruc': 'ruc',
                'name_empresa': 'name_empresa'
            }
            
            # Aplicar el renombrado
            resultado = resultado.rename(columns=mapping)
            
            # Guardar en SQLite
            conn = sqlite3.connect(db_path)
            resultado.to_sql('representantes', conn, if_exists='append', index=False)
            conn.close()
            return True, ruc
        
        return False, ruc
    except:
        pass

# a = procesar_ruc("20493354079")
# print(a)
def main(wokers = 2):
    
    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Cargar datos y filtrar
    print("Cargando datos...")
    df = pd.read_csv(DATA_PATH)
    df_empresas = df[df['is_ruc_empresa'] == 1]
    
    # Obtener lista de RUCs únicos
    rucs_totales = df_empresas['documento_identidad'].unique().tolist()
    print(f"Se encontraron {len(rucs_totales)} RUCs únicos en total")
    
    # Conectar a la BD para obtener los RUCs ya procesados
    conn = sqlite3.connect(DB_PATH)
    
    # Verificar si la tabla existe
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='representantes'")
    tabla_existe = cursor.fetchone()
    
    rucs_procesados = []
    if tabla_existe:
        # Obtener los RUCs ya procesados
        rucs_procesados_df = pd.read_sql("SELECT DISTINCT ruc FROM representantes", conn)
        if not rucs_procesados_df.empty:
            rucs_procesados = rucs_procesados_df['ruc'].tolist()
    
    conn.close()
    
    # Filtrar los RUCs que faltan procesar
    rucs_pendientes = [ruc for ruc in rucs_totales if ruc not in rucs_procesados]
    
    print(f"RUCs ya procesados: {len(rucs_procesados)}")
    print(f"RUCs pendientes de procesar: {len(rucs_pendientes)}")
    
    if not rucs_pendientes:
        print("No hay RUCs nuevos para procesar.")
        return
    
    # Procesar en paralelo con hilos
    resultados = []

    with ThreadPoolExecutor(max_workers=wokers) as executor:
        # Preparar argumentos para cada trabajo
        jobs = [(ruc, DB_PATH) for ruc in rucs_pendientes]
        
        # Ejecutar y mostrar progreso
        for resultado in tqdm(executor.map(lambda x: procesar_ruc(*x), jobs), total=len(jobs)):
            pass

if __name__ == "__main__":
    main(2)