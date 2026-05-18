from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import heapq
from collections import Counter

app = Flask(__name__)
CORS(app)

class NodoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.izq = None
        self.der = None

    def __lt__(self, otro):
        return self.freq < otro.freq

def construir_arbol(texto):
    frecuencias = Counter(texto)
    heap = [NodoHuffman(c, f) for c, f in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        izq = heapq.heappop(heap)
        der = heapq.heappop(heap)
        padre = NodoHuffman(None, izq.freq + der.freq)
        padre.izq = izq
        padre.der = der
        heapq.heappush(heap, padre)

    return heap[0]

def generar_codigos(nodo, prefijo="", tabla={}):
    if nodo is None:
        return
    if nodo.char is not None:
        tabla[nodo.char] = prefijo
        return
    generar_codigos(nodo.izq, prefijo + "0", tabla)
    generar_codigos(nodo.der, prefijo + "1", tabla)
    return tabla

def comprimir(texto, tabla):
    return "".join(tabla[c] for c in texto)

def descomprimir(bits, arbol):
    resultado = []
    nodo = arbol
    for bit in bits:
        nodo = nodo.izq if bit == "0" else nodo.der
        if nodo.char is not None:
            resultado.append(nodo.char)
            nodo = arbol
    return "".join(resultado)

base_dir = os.path.dirname(__file__)
ruta = os.path.join(base_dir, "data", "phishing_data.csv")

urls_raw = []
with open(ruta, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['status'] == 'phishing':
            urls_raw.append(row['url'])

texto_completo = "\n".join(urls_raw)
arbol_huffman  = construir_arbol(texto_completo)
tabla_codigos  = generar_codigos(arbol_huffman)

blacklist_comprimida = [comprimir(url, tabla_codigos) for url in urls_raw]

blacklist = [descomprimir(b, arbol_huffman) for b in blacklist_comprimida]

print(f"URLs cargadas:    {len(blacklist)}")
print(f"Tamaño original:  {len(texto_completo)} chars")
print(f"Tamaño comprimido:{sum(len(b) for b in blacklist_comprimida)} bits")


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