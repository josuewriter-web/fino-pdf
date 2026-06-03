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
        # 1. Entramos a la página de historial del BCV
        url = "https://www.bcv.org.ve/sistema-financiero/tipo-de-cambio-oficial-del-banco-central-de-venezuela"
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        tabla = soup.find("table")
        tasa_hoy = "0"
        
        # 2. Conseguimos el número del día de hoy en Venezuela (ejemplo: "03")
        zona_bcv = timezone(timedelta(hours=-4))
        hoy = datetime.now(zona_bcv)
        dia_buscado = hoy.strftime("%d") 
        
        if tabla:
            filas = tabla.find_all("tr")
            for fila in filas:
                celdas = fila.find_all("td")
                if len(celdas) >= 2:
                    texto_fecha = celdas[0].text.strip()
                    # Si la fila tiene el número del día de hoy, agarramos esa tasa
                    if dia_buscado in texto_fecha:
                        tasa_hoy = celdas[-1].text.strip().replace(",", ".")
                        break
            
            # Fallback: Si es fin de semana y hoy no aparece, agarramos la tasa más reciente
            if tasa_hoy == "0" and len(filas) > 1:
                primera_fila_datos = filas[1].find_all("td")
                if primera_fila_datos:
                    tasa_hoy = primera_fila_datos[-1].text.strip().replace(",", ".")
        
        # 3. Creamos la fecha bonita para tu reporte
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        fecha_bonita = f"{dias[hoy.weekday()]}, {hoy.strftime('%d')} {meses[hoy.month - 1]} {hoy.year}"
        
        return {"tasa": tasa_hoy, "fecha": fecha_bonita}
        
    except Exception as e:
        return {"tasa": "0", "fecha": "Error"}
