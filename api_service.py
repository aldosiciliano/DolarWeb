import requests
import logging

logger = logging.getLogger(__name__)

def get_dolar_blue():
    url = 'https://magicloops.dev/api/loop/0b4f6442-c2c8-46d2-90ea-9665ebb4c3f4/run'
    try:
        logger.debug(f"Realizando petición GET a {url}")
        response = requests.get(url)
        logger.debug(f"Código de estado: {response.status_code}")
        logger.debug(f"Respuesta: {response.text}")
        
        if response.status_code == 200:
            return response.json()
        logger.error(f"Error en la API: Status code {response.status_code}")
        return None
    except requests.RequestException as e:
        logger.error(f"Error al llamar a la API: {str(e)}")
        return None