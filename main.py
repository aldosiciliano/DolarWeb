from flask import Flask, render_template, make_response
from api_service import get_dolar_blue
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def home():
    # Agregamos timestamp para evitar cache
    timestamp = int(time.time())
    
    data = get_dolar_blue()
    if data:
        compra = data['compra']
        venta = data['venta']
        try:
            fecha_iso = data['fechaActualizacion']
            fecha = datetime.fromisoformat(fecha_iso.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
        except Exception as e:
            fecha = "No disponible"
    else:
        compra = "N/A"
        venta = "N/A"
        fecha = "No disponible"
    
    response = make_response(render_template('index.html', 
                                           compra=compra, 
                                           venta=venta, 
                                           fecha=fecha,
                                           timestamp=timestamp))
    
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

app.debug = False

if __name__ == '__main__':
    app.run()

