import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obtener_tasa_y_fecha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        # 1. Entramos a la página del historial de tasas del BCV
        url = "https://www.bcv.org.ve/sistema-financiero/tipo-de-cambio-oficial-del-banco-central-de-venezuela"
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscamos la tabla con las fechas
        tabla = soup.find("table")
        
        # 2. Conseguimos la fecha de hoy en Venezuela
        zona_bcv = timezone(timedelta(hours=-4))
        hoy = datetime.now(zona_bcv)
        
        # Formatos de fecha que usa el BCV (ejemplo: 03-06-2026 o 03/06/2026)
        fecha_buscar_1 = hoy.strftime("%d-%m-%Y")
        fecha_buscar_2 = hoy.strftime("%d/%m/%Y")
        
        tasa_hoy = "0"
        
        # 3. Buscamos la fila exacta que tenga la fecha de hoy
        if tabla:
            filas = tabla.find_all("tr")
            for fila in filas:
                texto_fila = fila.text.strip()
                if fecha_buscar_1 in texto_fila or fecha_buscar_2 in texto_fila:
                    celdas = fila.find_all("td")
                    if celdas:
                        # El precio del dólar siempre es el último número de la fila
                        tasa_hoy = celdas[-1].text.strip().replace(",", ".")
                        break
        
        # 4. Creamos la fecha bonita en español para tu reporte
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        nombre_dia = dias[hoy.weekday()]
        nombre_mes = meses[hoy.month - 1]
        fecha_bonita = f"{nombre_dia}, {hoy.strftime('%d')} {nombre_mes} {hoy.year}"
        
        return {"tasa": tasa_hoy, "fecha": fecha_bonita}
        
    except Exception as e:
        return {"tasa": "0", "fecha": "Error"}
