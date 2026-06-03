import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

def obtener_tasa_y_fecha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        # 1. Vamos a la página de la tabla histórica del BCV
        url = "https://www.bcv.org.ve/sistema-financiero/tipo-de-cambio-oficial-del-banco-central-de-venezuela"
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 2. Conseguimos la fecha de HOY en Venezuela
        zona_bcv = timezone(timedelta(hours=-4))
        hoy = datetime.now(zona_bcv)
        fecha_hoy = hoy.strftime("%d-%m-%Y") # Ejemplo: 03-06-2026
        
        tasa_hoy = "0"
        
        # 3. Buscamos en la tabla la fila que tenga la fecha de hoy
        filas = soup.find_all("tr")
        for fila in filas:
            texto_fila = fila.text.strip()
            if fecha_hoy in texto_fila:
                celdas = fila.find_all("td")
                if celdas:
                    # El dólar siempre es el último valor de la fila
                    tasa_hoy = celdas[-1].text.strip().replace(",", ".")
                    break
        
        # Si es fin de semana y no hay fila de hoy, agarramos el último precio guardado
        if tasa_hoy == "0":
            for fila in filas:
                celdas = fila.find_all("td")
                if len(celdas) >= 2:
                    tasa_hoy = celdas[-1].text.strip().replace(",", ".")
                    break

        # 4. Creamos la fecha bonita para tu reporte
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        nombre_dia = dias[hoy.weekday()]
        nombre_mes = meses[hoy.month - 1]
        fecha_bonita = f"{nombre_dia}, {hoy.strftime('%d')} {nombre_mes} {hoy.year}"
        
        return {"tasa": tasa_hoy, "fecha": fecha_bonita}
    except Exception as e:
        return {"tasa": "0", "fecha": "Error"}
