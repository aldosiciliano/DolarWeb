from flask import Flask, render_template
from api_service import get_dolar_blue
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    data = get_dolar_blue()
    print("Datos completos:", data)  # Agregamos este print para debug
    
    if data:
        compra = data['compra']
        venta = data['venta']
        try:
            fecha_iso = data['fechaActualizacion']
            print("Fecha ISO:", fecha_iso)  # Debug de la fecha
            fecha = datetime.fromisoformat(fecha_iso.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
            print("Fecha formateada:", fecha)  # Debug de la fecha formateada
        except Exception as e:
            print("Error al procesar fecha:", e)  # Debug de errores
            fecha = "No disponible"
    else:
        compra = "N/A"
        venta = "N/A"
        fecha = "No disponible"
    
    return render_template('index.html', compra=compra, venta=venta, fecha=fecha)

if __name__ == '__main__':
    app.run(debug=True)

