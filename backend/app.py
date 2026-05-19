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


def generar_codigos(nodo, prefijo="", tabla=None):
    if tabla is None:
        tabla = {}
    if nodo is None:
        return tabla
    if nodo.char is not None:
        tabla[nodo.char] = prefijo
        return tabla
    generar_codigos(nodo.izq, prefijo + "0", tabla)
    generar_codigos(nodo.der, prefijo + "1", tabla)
    return tabla


def comprimir(texto, tabla):
    return "".join(tabla[c] for c in texto if c in tabla)


def descomprimir(bits, arbol):
    resultado = []
    nodo = arbol
    for bit in bits:
        nodo = nodo.izq if bit == "0" else nodo.der
        if nodo.char is not None:
            resultado.append(nodo.char)
            nodo = arbol
    return "".join(resultado)

def normalizar(url: str) -> str:
    url = url.strip()
    url = url.split("#")[0]
    url = url.rstrip("/")
    if url.startswith("https://"):
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]
    return url

#cargamos el dataset
base_dir = os.path.dirname(__file__)
ruta = os.path.join(base_dir, "data", "dataset_web_26.csv")

urls_peligrosas  = []  # phishing/malware  → riesgo alto - original
urls_sospechosas = []  # defacement          → riesgo sospechoso - orginal

with open(ruta, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tipo = row['type']
        if tipo in ('phishing', 'malware'):
            urls_peligrosas.append(normalizar(row['url']))
        elif tipo == 'defacement':
            urls_sospechosas.append(normalizar(row['url']))

texto_completo = "\n".join(urls_peligrosas + urls_sospechosas)
arbol_huffman  = construir_arbol(texto_completo)
tabla_codigos  = generar_codigos(arbol_huffman)

blacklist_peligrosas  = [comprimir(url, tabla_codigos) for url in urls_peligrosas] #lista comprimida
blacklist_sospechosas = [comprimir(url, tabla_codigos) for url in urls_sospechosas] #lista comprimida

chars_peligrosas  = sum(len(u) for u in urls_peligrosas)
chars_sospechosas = sum(len(u) for u in urls_sospechosas)
bits_peligrosas   = sum(len(b) for b in blacklist_peligrosas)
bits_sospechosas  = sum(len(b) for b in blacklist_sospechosas)

print(f"url's de phishing+malware): {len(blacklist_peligrosas)}")
print(f"Original: {chars_peligrosas * 8} bits -> Comprimido: {bits_peligrosas} bits")
print(f"url's defacement: {len(blacklist_sospechosas)}")
print(f"Original: {chars_sospechosas * 8} bits -> Comprimido: {bits_sospechosas} bits")

cache_urls = {}

def clasificar(url: str) -> str:
    url = normalizar(url)

    if url in cache_urls:
        print(f"url consultado en cache: {url}")
        return cache_urls[url]

    if any(c not in tabla_codigos for c in url):
        cache_urls[url] = "bajo"
        return "bajo"

    url_comprimida = comprimir(url, tabla_codigos)

    #fuerza brura, recorremos con indice y valor
    for i, bad_bits in enumerate(blacklist_peligrosas):
        bad_url = urls_peligrosas[i]
        if url_comprimida == bad_bits or url.endswith("." + bad_url):
            cache_urls[url] = "alto"
            return "alto"

    for i, bad_bits in enumerate(blacklist_sospechosas):
        bad_url = urls_sospechosas[i]
        if url_comprimida == bad_bits or url.endswith("." + bad_url):
            cache_urls[url] = "sospechoso"
            return "sospechoso"

    cache_urls[url] = "bajo"
    return "bajo"


@app.route("/")
def home():
    return "El back funciona"

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    url  = data.get("url", "")
    print(f"[DEBUG] URL recibida:    '{url}'")
    print(f"[DEBUG] URL normalizada: '{normalizar(url)}'")
    return jsonify({"riesgo": clasificar(url)})


if __name__ == "__main__":
    app.run(debug=True)