from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'datos.json'

# Función para asegurar que el archivo existe
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f: json.dump([], f)
    with open(DATA_FILE, 'r') as f: return json.load(f)

def guardar_datos(datos):
    with open(DATA_FILE, 'w') as f: json.dump(datos, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nueva_apuesta = {
            'nombre': request.form['nombre'],
            'partido': request.form['partido'],
            'local': request.form['local'],
            'visitante': request.form['visitante'],
            'estado': 'Pendiente'
        }
        datos = cargar_datos()
        datos.append(nueva_apuesta)
        guardar_datos(datos)
        return "Apuesta enviada correctamente. <a href='/'>Volver</a>"
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', apuestas=cargar_datos())

@app.route('/validar/<int:index>')
def validar(index):
    datos = cargar_datos()
    datos[index]['estado'] = 'Validado'
    guardar_datos(datos)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)