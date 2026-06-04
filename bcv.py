import requests
from datetime import datetime, timezone, timedelta

def obtener_tasa_y_fecha():
    tasa_hoy = "0"
    
    # Usamos la base de datos pública que sí funcionó
    try:
        url = "https://ve.dolarapi.com/v1/dolares/oficial"
        respuesta = requests.get(url, timeout=10).json()
        tasa_hoy = str(respuesta["promedio"]).replace(",", ".")
    except:
        tasa_hoy = "0"

    # Creamos la fecha bonita
    zona_bcv = timezone(timedelta(hours=-4))
    hoy = datetime.now(zona_bcv)
    
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    fecha_bonita = f"{dias[hoy.weekday()]}, {hoy.strftime('%d')} {meses[hoy.month - 1]} {hoy.year}"
    
    return {"tasa": tasa_hoy, "fecha": fecha_bonita}
