from flask import Flask, request
import csv

app = Flask(__name__)

@app.route('/guardar-datos', methods=['POST'])
def guardar_datos():
    pot_value = request.args.get('pot')
    led_value = request.args.get('led')
    
    with open('datos.csv', 'a', newline='') as csvfile:
        fieldnames = ['pot', 'led']
        writer = csv.DictWriter(csvfile, fieldnamees=fieldnames)

        # Si el archivo no existe, escribe los encabezados
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({'pot': pot_value, 'led': led_value})
    
    return 'Datos guardados'

if __name__ == '__main__':
    app.run(debug=True)
    