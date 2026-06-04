import requests
import re
from datetime import datetime, timezone, timedelta

def obtener_tasa_y_fecha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    tasa_hoy = "0"
    
    try:
        # 1. ¡Tu idea! Entramos directo a la página de tasas.
        url = "https://alcambio.app/tasas"
        response = requests.get(url, headers=headers, timeout=10)
        
        # Buscamos la palabra BCV y el número
        match = re.search(r'(?i)bcv.*?(\d{2,3}[\.,]\d{2,4})', response.text)
        if match:
            tasa_hoy = match.group(1).replace(",", ".")
            
    except:
        pass
        
    # 2. SEGURO DE VIDA: Si AlCambio falla, usamos una base de datos libre
    if tasa_hoy == "0":
        try:
            url_respaldo = "https://ve.dolarapi.com/v1/dolares/oficial"
            res = requests.get(url_respaldo, timeout=10).json()
            tasa_hoy = str(res["promedio"]).replace(",", ".")
        except:
            tasa_hoy = "0"

    # 3. Tu fecha en español
    zona_bcv = timezone(timedelta(hours=-4))
    hoy = datetime.now(zona_bcv)
    
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    fecha_bonita = f"{dias[hoy.weekday()]}, {hoy.strftime('%d')} {meses[hoy.month - 1]} {hoy.year}"
    
    return {"tasa": tasa_hoy, "fecha": fecha_bonita}
