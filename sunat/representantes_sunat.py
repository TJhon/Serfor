from bs4 import BeautifulSoup
import requests
import random
import string
import pandas as pd

def generate_key(length=52):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def consultar_ruc(ruc):
    try:
        session = requests.Session()

        # Paso 1: Acceder a la página inicial para establecer cookies
        url_inicio = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp"
        session.get(url_inicio, headers={"User-Agent": "Mozilla/5.0"})

        # Paso 2: Generar token local
        token = generate_key(52)

        # Paso 3: Hacer POST principal para obtener HTML con datos
        url_post = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
        headers_post = {
            "User-Agent": "Mozilla/5.0",
            "Referer": url_inicio,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        data_post = {
            "accion": "consPorRuc",
            "razSoc": "",
            "nroRuc": ruc,
            "nrodoc": "",
            "token": token,
            "contexto": "ti-it",
            "modo": "1",
            "rbtnTipo": "1",
            "search1": ruc,
            "tipdoc": "1",
            "search2": "",
            "search3": "",
            "codigo": ""
        }

        response = session.post(url_post, headers=headers_post, data=data_post)
        if not response.ok:
            return f"Error en primera consulta: {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')

        # Paso 4: Extraer nombre de empresa (desRuc)
        nro_ruc_input = soup.find("input", {"name": "nroRuc"})
        des_ruc_input = soup.find("input", {"name": "desRuc"})

        if not (nro_ruc_input and des_ruc_input):
            return "No se encontró desRuc/nroRuc en el HTML de respuesta."

        nro_ruc = nro_ruc_input.get("value")
        des_ruc = des_ruc_input.get("value")

        # Paso 5: Segunda solicitud para obtener representantes legales
        data_rep_leg = {
            "accion": "getRepLeg",
            "contexto": "ti-it",
            "modo": "1",
            "desRuc": des_ruc,
            "nroRuc": nro_ruc
        }

        response_rep = session.post(url_post, headers=headers_post, data=data_rep_leg)

        soup = BeautifulSoup(response_rep.content, 'html.parser')
        headers = [th.get_text(strip=True) for th in soup.find_all("th")]

        # Extraer filas
        rows = []
        for tr in soup.find_all("tbody")[0].find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            rows.append(cells)

        # Crear DataFrame
        df = pd.DataFrame(rows, columns=headers)
        df['ruc'] = ruc
        df['name_empresa'] = des_ruc
        return df

    except:
        return None
if __name__ == "__main__":
    # 🔍 Ejemplo de uso
    html_representantes = consultar_ruc("20104094971")
    print(html_representantes)

