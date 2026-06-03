import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

def obtener_tasa_y_fecha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        url = "https://alcambio.app"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        tasa_hoy = "0"
        
        # 1. Buscamos el contenedor específico del BCV en la interfaz de AlCambio
        # Generalmente usan tarjetas o secciones que asocian el texto "BCV" con el precio
        for contenedor in soup.find_all(["div", "tr", "p"]):
            texto = contenedor.get_text().upper()
            if "BCV" in texto:
                # Extraemos los números con decimales que estén en ese mismo bloque
                import re
                numeros = re.findall(r'\d+[\.,]\d+', texto)
                if numeros:
                    tasa_hoy = numeros[0].replace(",", ".")
                    break
        
        # Fallback: Si el diseño cambia un poco, extrae el primer decimal grande de la página
        if tasa_hoy == "0":
            import re
            todos_los_numeros = re.findall(r'\d+[\.,]\d+', soup.get_text())
            if todos_los_numeros:
                tasa_hoy = todos_los_numeros[0].replace(",", ".")

        # 2. Fecha local de Venezuela garantizada para tu reporte Fino
        zona_bcv = timezone(timedelta(hours=-4))
        hoy = datetime.now(zona_bcv)
        
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        fecha_bonita = f"{dias[hoy.weekday()]}, {hoy.strftime('%d')} {meses[hoy.month - 1]} {hoy.year}"
        
        return {"tasa": tasa_hoy, "fecha": fecha_bonita}
        
    except Exception as e:
        return {"tasa": "0", "fecha": f"Error: {str(e)}"}
