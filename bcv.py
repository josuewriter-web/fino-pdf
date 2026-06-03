import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timezone, timedelta

def obtener_tasa_y_fecha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        # Entramos a la nueva página
        url = "https://alcambio.app"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Guardamos todo el texto de la página en minúsculas
        texto_pagina = soup.get_text().lower()
        tasa_hoy = "0"
        
        # Buscamos la palabra "bcv" y el primer número con decimales que aparezca después
        match = re.search(r'bcv.*?(\d+[\.,]\d+)', texto_pagina, re.DOTALL)
        if match:
            tasa_hoy = match.group(1).replace(",", ".")
        else:
            # Si cambia el diseño, agarramos el primer número decimal que encontremos
            todos_los_numeros = re.findall(r'\d+[\.,]\d+', texto_pagina)
            if todos_los_numeros:
                tasa_hoy = todos_los_numeros[0].replace(",", ".")
        
        # Como la página tiene la tasa de hoy, usamos la fecha actual de Venezuela
        zona_bcv = timezone(timedelta(hours=-4))
        hoy = datetime.now(zona_bcv)
        
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        fecha_bonita = f"{dias[hoy.weekday()]}, {hoy.strftime('%d')} {meses[hoy.month - 1]} {hoy.year}"
        
        return {"tasa": tasa_hoy, "fecha": fecha_bonita}
    except:
        return {"tasa": "0", "fecha": "Error"}
