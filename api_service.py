import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_dolar_blue():
    url = "https://dolarhoy.com/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Diccionario para almacenar las cotizaciones
            dollar_quotes = {}
            
            # Lista de tipos de dólar que queremos obtener
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
                    print(f"Título encontrado: {titulo}")
                    
                    # Identificar el tipo de dólar
                    tipo_encontrado = None
                    for tipo_key, alternativas in tipos_dolar.items():
                        if any(alt.lower() in titulo.lower() for alt in alternativas):
                            tipo_encontrado = tipo_key
                            # Si encontramos "Contado con Liqui", lo mapeamos a "Dólar CCL"
                            if "contado con liqui" in titulo.lower():
                                tipo_encontrado = "Dólar CCL"
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
                                compra = compra_val.text.strip()
                        
                        if venta_elem:
                            venta_val = venta_elem.find("div", class_="val")
                            if venta_val:
                                venta = venta_val.text.strip()
                        
                        # Guardar en el diccionario
                        dollar_quotes[tipo_encontrado] = {
                            'Compra': compra,
                            'Venta': venta
                        }
            
            # Debug: imprimir cotizaciones encontradas
            print("Cotizaciones encontradas:", dollar_quotes)
            
            return {
                'dollar_quotes': dollar_quotes,
                'last_updated': datetime.now().strftime('%d/%m/%y %I:%M %p')
            }
        return None
    except Exception as e:
        print(f"Error en el scraping: {str(e)}")
        return None