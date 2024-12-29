import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from datetime import timedelta
import os

def get_dolar_blue():
    url = "https://dolarhoy.com/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            
            dollar_quotes = {}
            
            
            tipos_dolar = {
                "Dólar Blue": ["Dólar Blue", "dólar blue"],
                "Dólar Oficial": ["Dólar Oficial", "dólar oficial"],
                "Dólar MEP": ["Dólar MEP", "MEP", "Bolsa"],
                "Dólar CCL": ["Contado con Liqui", "Contado con liqui", "CCL", "Dólar CCL"],
                "Dólar Cripto": ["Dólar Cripto", "Cripto"],
                "Dólar Tarjeta": ["Dólar Tarjeta", "tarjeta"]
            }
            
            # Buscar bloques con la clase "tile is-child"
            bloques = soup.find_all("div", class_="tile is-child")
            for bloque in bloques:
                titulo_elem = bloque.find("a", class_="title")
                if titulo_elem:
                    titulo = titulo_elem.text.strip()
                    
                    # Identificar el tipo de dólar
                    tipo_encontrado = None
                    for tipo_key, alternativas in tipos_dolar.items():
                        if any(alt.lower() in titulo.lower() for alt in alternativas):
                            tipo_encontrado = tipo_key
                            break
                    
                    if tipo_encontrado:
                        # Extraer valores de compra y venta
                        compra_elem = bloque.find("div", class_="compra")
                        venta_elem = bloque.find("div", class_="venta")
                        
                        compra = "N/A"
                        venta = "N/A"
                        
                        if compra_elem:
                            compra_val = compra_elem.find("div", class_="val")
                            if compra_val:
                                # Eliminar el símbolo $ y espacios
                                compra = compra_val.text.strip().replace('$', '').strip()
                        
                        if venta_elem:
                            venta_val = venta_elem.find("div", class_="val")
                            if venta_val:
                                # Eliminar el símbolo $ y espacios
                                venta = venta_val.text.strip().replace('$', '').strip()
                        
                        # Guardar en el diccionario
                        dollar_quotes[tipo_encontrado] = {
                            'Compra': compra,
                            'Venta': venta
                        }
            
            # Configurar zona horaria de Argentina
            argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
            hora_argentina = datetime.now(argentina_tz)
            
            return {
                'dollar_quotes': dollar_quotes,
                'last_updated': hora_argentina.strftime('%d/%m/%y %I:%M %p')
            }
        return None
    except Exception as e:
        print(f"Error en el scraping: {str(e)}")
        return None