
"""
HISTORIAL DE INFRACTORES DE DATOS ABIERTOS
"""

import requests, os
from tqdm import tqdm
import pandas as pd


save_path = input_path = "data/raw/historial_infractores"
os.makedirs(save_path, exist_ok=True)
output_path = "data/raw"
os.makedirs(output_path, exist_ok=True)


def download_data ():
    serfor_infractores = 'https://datosabiertos.gob.pe/api/3/action/package_show?id=889a66c9-943a-4616-94cd-83c66ddd9f24'

    response = requests.get(serfor_infractores).json()

    resources = response.get('result', [])[0].get('resources', [])

    url_resources = [resource.get('url') for resource in resources]


    for url in tqdm(url_resources):
        file_name = os.path.join(save_path, os.path.basename(url))  # Usa el nombre original del archivo

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Lanza un error si la solicitud falla

            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Archivo guardado en {file_name}")

        except requests.RequestException as e:
            print(f"Error al descargar {url}: {e}")

download_data()

output_file = os.path.join(output_path, "infractores_historial.csv")

column_mapping = {
    "Numero": "numero",
    "Infractor": "infractor",
    "DocumentoIdentidad": "documento_identidad",
    "tituloHab": "titulo_habilitante",
    "Resolucion": "resolucion_sancionadora",
    "FechaResolucion": "fecha_resolucion",
    "OrganoSancionador": "organo_sancionador",
    "AmbitoInfraccion": "ambito_infraccion",
    "Número": "numero",
    "Documento de Identidad": "documento_identidad",
    "Título habilitante": "titulo_habilitante",
    "Resolución sancionadora": "resolucion_sancionadora",
    "Fecha Resolución": "fecha_resolucion",
    "Órgano Sancionador": "organo_sancionador",
    "Ámbito de la  Infracción": "ambito_infraccion"
}


csv_files = [f for f in os.listdir(input_path) if f.endswith(".csv")]

# Leer y combinar los CSV
dataframes = []

for file in csv_files:
    file_path = os.path.join(input_path, file)
    try:
        df = pd.read_csv(file_path)  # Ajusta encoding si es necesario
    except:
        df = pd.read_csv(file_path, delimiter=';')
        # dataframes.append(df)
    df = df.rename(columns=column_mapping)

    dataframes.append(df)
# Concatenar y guardar el archivo final
if dataframes:
    merged_df = pd.concat(dataframes, ignore_index=True).drop_duplicates()
    merged_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Archivo combinado guardado en {output_file}")
else:
    print("No se encontraron archivos CSV para combinar.")


