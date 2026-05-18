from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import heapq
from collections import Counter

app = Flask(__name__)
CORS(app)

class nodoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.izq = None
        self.der = None
    
    def __lt__(self, otro):
        return self.freq < otro.freq

def construirArbol(texto):
    frecuencias = Counter(texto)
    heap = [nodoHuffman(c, f) for c, f in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        izq = heapq.heappop(heap)
        der = heapq.heappop(heap)
        padre = nodoHuffman(None, izq.freq + der.freq)
        padre.izq = izq
        padre.der = der
        heapq.heappush(heap, padre)

    return heap[0]

def generarCodigos(nodo, prefijo="", tabla=None): #aqui se deberia de generar la tabla de codigos
    if tabla is None:
        tabla = {}
    if nodo is None:
        return tabla
    if nodo.char is not None:
        tabla[nodo.char] = prefijo
        return tabla
    generarCodigos(nodo.izq, prefijo + "0", tabla)
    generarCodigos(nodo.der, prefijo + "1", tabla)
    return tabla

def comprimir(texto, tabla): #ya se comprime el texto aqui
    return "".join(tabla[c] for c in texto if c in tabla)

def descomprimir(bits, arbol):
    resultado = []
    nodo = arbol #no se te olvide la comparacion del nodo por lo generado hasta el arbol porfa
    for bit in bits:
        nodo = nodo.izq if bit == "0" else nodo.der
        if nodo.char is not None:
            resultado.append(nodo.char)
            nodo = arbol
    return "".join(resultado)


base_dir = os.path.dirname(__file__)
ruta = os.path.join(base_dir,"data", "dataset_web_26.csv")

urls_crudos = []
clasificacion_urls = {}

#cargamos el dataset
with open(ruta, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    print(reader.fieldnames)

    for row in reader:
        url = row['url'].strip()
        tipo = row['type'].strip().lower()

        urls_crudos.append(url)
        clasificacion_urls[url] = tipo

texto_completo = "\n".join(urls_crudos)
arbol_huffman = construirArbol(texto_completo)
tabla_codigos = generarCodigos(arbol_huffman)

blacklist_comprimida = []

for url,tipo in clasificacion_urls.items():
    url_comp = comprimir(url,tabla_codigos)
    blacklist_comprimida.append((url_comp, tipo))

blacklist = [descomprimir(b, arbol_huffman) for b in blacklist_comprimida]

print(f"urls cargadas: {len(blacklist_comprimida)} links maliciosos")
print(f"tamaño original: {len(texto_completo)} caracteres")
print(f"tamaño comprimido: {sum(len(b[0]) for b in blacklist_comprimida)} bits")

#despues de comprimir busca en la lista
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

    riesgo = es_malicioso(url)

    return jsonify({
        "url": url,
        "riesgo": riesgo
    })
    

if __name__ == "__main__":
    app.run(debug=True)