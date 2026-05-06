from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(__file__)
ruta = os.path.join(base_dir,"data", "phishing_data.csv")

blacklist = []

#cargamos el dataset
with open(ruta, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    print(reader.fieldnames)
    for row in reader:
        if row['status'] == 'phishing':
            blacklist.append(row['url'])

print(f"se cargo del data set. {len(blacklist)} links maliciosos")

#implementacion de fuerza bruta
def es_malicioso(url):
    for bad_url in blacklist:
        if bad_url in url:
            return True
    return False

@app.route("/")
def home():
    return "EL back funciona"

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    url = data.get("url", "")

    if es_malicioso(url):
        return jsonify({"riesgo": "alto"})
    else:
        return jsonify({"riesgo": "bajo"})
    

if __name__ == "__main__":
    app.run(debug=True)