import requests
from bs4 import BeautifulSoup

def obtener_tasa_y_fecha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        url = "https://www.bcv.org.ve/"
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        box_dolar = soup.find(id="dolar")
        tasa = box_dolar.find("strong").text.strip() if box_dolar else "0"
        tasa_limpia = tasa.replace(",", ".")
        
        box_fecha = soup.find(class_="date-display-single")
        fecha = box_fecha.text.strip() if box_fecha else "No encontrada"
        
        return {"tasa": tasa_limpia, "fecha": fecha}
    except Exception as e:
        return {"tasa": "0", "fecha": "Error"}
