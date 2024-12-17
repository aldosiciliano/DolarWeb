import requests

def get_dolar_blue():
    url = "https://dolarapi.com/v1/dolares/blue"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None