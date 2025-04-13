import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# === Carpeta de descarga personalizada (por parámetro) ===
directorio_descargas = "./data/raw/personal_estado"  # <-- cambia por tu ruta o pásalo como argumento

# Asegurarse que existe
os.makedirs(directorio_descargas, exist_ok=True)

# === Configurar opciones de Chrome ===
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

prefs = {
    "download.default_directory": os.path.abspath(directorio_descargas),  # ruta absoluta
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# === Iniciar el navegador con las opciones configuradas ===
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === URL que quieres abrir ===
url1 = 'https://www.transparencia.gob.pe/personal/pte_transparencia_personal_genera.aspx?id_entidad=10766&in_anno_consulta=2009&ch_mes_consulta=11&ch_tipo_regimen=0&vc_dni_funcionario=&vc_nombre_funcionario=&ch_tipo_descarga=1'

url2 = 'https://www.transparencia.gob.pe/personal/pte_transparencia_personal_genera.aspx?id_entidad=10766&in_anno_consulta=2023&ch_mes_consulta=01&ch_tipo_regimen=0&vc_dni_funcionario=&vc_nombre_funcionario=&ch_tipo_descarga=1'

# Abrir página principal (por si lo necesitas)
driver.get("https://www.transparencia.gob.pe/")
time.sleep(2)

# Ir directamente al link de descarga

for i in [url1, url2, url2, url2, url2]:
    try:
        driver.get(i)
        time.sleep(1)  # espera suficiente para la descarga
    except:
        pass
# (Opcional) cerrar navegador
driver.quit()
