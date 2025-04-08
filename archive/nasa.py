import os
from ftplib import FTP

# Configuración de credenciales y servidor FTP
FTP_HOST = "fuoco.geog.umd.edu"
FTP_USER = "fire"
FTP_PASS = "burnt"
MODIS_PATH = "modis/C6/mcd14ml/"
CMG_PATH = "modis/C6/cmg/monthly/hdf/"
from ftplib import FTP_TLS
# Directorio local para almacenar los archivos
data_dir = os.path.expanduser("~/.bowerbird")
os.makedirs(data_dir, exist_ok=True)

def download_files(ftp_path, local_dir):
    with FTP_TLS(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        ftp.prot_p() 
            
        filenames = ftp.nlst()
        for filename in filenames:
            if filename.endswith(".gz"):  # Filtrar solo los archivos .gz
                local_file = os.path.join(local_dir, filename)
                if not os.path.exists(local_file):
                    with open(local_file, "wb") as f:
                        ftp.retrbinary(f"RETR {filename}", f.write)
                    print(f"Descargado: {filename}")
                else:
                    print(f"Ya existe: {filename}")

# Descargar archivos de MODIS y CMG
download_files(MODIS_PATH, data_dir)
download_files(CMG_PATH, data_dir)

print("Descarga completa.")
