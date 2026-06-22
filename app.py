from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'datos.json'

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return {"partido": "Esperando admin...", "cuota": 0, "apuestas": []}
    with open(DATA_FILE, 'r') as f: return json.load(f)

def guardar_datos(datos):
    with open(DATA_FILE, 'w') as f: json.dump(datos, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    datos = cargar_datos()
    if request.method == 'POST':
        nueva_apuesta = {
            'nombre': request.form['nombre'],
            'local': request.form['local'],
            'visitante': request.form['visitante'],
            'comprobante': request.form['comprobante'],
            'estado': 'Pendiente'
        }
        datos['apuestas'].append(nueva_apuesta)
        guardar_datos(datos)
        return "Apuesta enviada. <a href='/'>Volver</a>"
    return render_template('index.html', datos=datos)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    datos = cargar_datos()
    if request.method == 'POST':
        datos['partido'] = request.form['partido']
        datos['cuota'] = request.form['cuota']
        guardar_datos(datos)
    return render_template('admin.html', datos=datos)

@app.route('/validar/<int:index>')
def validar(index):
    datos = cargar_datos()
    datos['apuestas'][index]['estado'] = 'Validado'
    guardar_datos(datos)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)