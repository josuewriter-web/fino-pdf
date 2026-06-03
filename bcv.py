import requests
from datetime import datetime, timezone, timedelta

def obtener_tasa_y_fecha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        # Consultamos directo a la API interna de AlCambio
        url = "https://api.alcambio.app/tasas"
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        
        tasa_hoy = "0"
        
        # Buscamos el valor del BCV dentro de la respuesta
        for item in datos.get("tasas", []):
            if item.get("moneda") == "USD" and item.get("fuente") == "BCV":
                tasa_hoy = str(item.get("precio", "0")).replace(",", ".")
                break
                
        # Si la estructura es diferente, buscamos por palabra clave
        if tasa_hoy == "0" and isinstance(datos, dict):
            for clave, valor in datos.items():
                if "bcv" in clave.lower() and isinstance(valor, (int, float)):
                    tasa_hoy = str(valor).replace(",", ".")
                    break

        # Fecha local de Venezuela garantizada para tu reporte Fino
        zona_bcv = timezone(timedelta(hours=-4))
        hoy = datetime.now(zona_bcv)
        
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        fecha_bonita = f"{dias[hoy.weekday()]}, {hoy.strftime('%d')} {meses[hoy.month - 1]} {hoy.year}"
        
        return {"tasa": tasa_hoy, "fecha": fecha_bonita}
        
    except Exception as e:
        # En caso de error, intentamos un método secundario rápido antes de rendirnos
        try:
            url_alt = "https://alcambio.app/api/tasas"
            res = requests.get(url_alt, headers=headers, timeout=5).json()
            tasa = str(res.get("bcv", res.get("USD_BCV", "0")))
            return {"tasa": tasa.replace(",", "."), "fecha": "Fecha Actualizada"}
        except:
            return {"tasa": "0", "fecha": f"Error: {str(e)}"}
