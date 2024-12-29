from flask import Flask, render_template, jsonify
from api_service import get_dolar_blue

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    data = get_dolar_blue()
    if data:
        return render_template('index.html', 
                             cotizaciones=data['dollar_quotes'],
                             ultima_actualizacion=data['last_updated'])
    return "Error al obtener cotizaciones"

@app.route('/conversor')
def conversor():
    return render_template('conversor.html')

@app.route('/get_cotizaciones')
def get_cotizaciones():
    data = get_dolar_blue()
    if data:
        return jsonify(data)
    return jsonify({"error": "No se pudieron obtener las cotizaciones"})

@app.route('/cotizaciones')
def cotizaciones():
    return render_template('cotizaciones.html')

if __name__ == '__main__':
    app.run(debug=True)

