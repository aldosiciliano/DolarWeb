from flask import Flask, render_template, jsonify
from api_service import get_dolar_blue
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def utility_processor():
    return dict(now=datetime.now)

@app.route('/')
def index():
    response = get_dolar_blue()
    if response and 'dollar_quotes' in response:
        cotizaciones = {}
        for tipo, valores in response['dollar_quotes'].items():
            cotizaciones[tipo] = {
                'compra': valores.get('Compra', 'N/A').replace('$', '').strip() if 'Compra' in valores else 'N/A',
                'venta': valores.get('Venta', 'N/A').replace('$', '').strip()
            }
        ultima_actualizacion = response.get('last_updated', '')
        return render_template('index.html', 
                             cotizaciones=cotizaciones,
                             ultima_actualizacion=ultima_actualizacion)
    return render_template('index.html', cotizaciones={}, ultima_actualizacion='')

@app.route('/get_cotizaciones')
def get_cotizaciones():
    response = get_dolar_blue()
    if response and 'dollar_quotes' in response:
        cotizaciones = {}
        for tipo, valores in response['dollar_quotes'].items():
            cotizaciones[tipo] = {
                'compra': valores.get('Compra', 'N/A').replace('$', '').strip() if 'Compra' in valores else 'N/A',
                'venta': valores.get('Venta', 'N/A').replace('$', '').strip()
            }
        return jsonify({
            'cotizaciones': cotizaciones,
            'ultima_actualizacion': response.get('last_updated', '')
        })
    return jsonify({'error': 'No se pudieron obtener las cotizaciones'})

if __name__ == '__main__':
    app.run(debug=True)

