# retrieve_information.py
# Este script permite realizar búsquedas de fragmentos relevantes en los guiones utilizando FAISS.

import faiss
import numpy as np
import json
import requests

# Cargar el índice FAISS y los metadatos
index = faiss.read_index("movie_scripts.index")

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# URL de la API para generar embeddings de la consulta
api_url = "http://tormenta.ing.puc.cl/api/embed"

def get_query_embedding(query):
    """
    Genera el embedding de una consulta utilizando la API 'nomic-embed-text'.
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "nomic-embed-text",
        "input": query
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return np.array(data["embeddings"][0]).astype("float32")  # Convertir a tipo float32 para FAISS
    else:
        print(f"Error en la API: {response.status_code}")
        return None

def search_similar_fragments(query, top_k=5):
    """
    Realiza una búsqueda de fragmentos similares dada una consulta.
    """
    query_embedding = get_query_embedding(query)
    if query_embedding is None:
        print("No se pudo generar el embedding de la consulta.")
        return []

    # Realizar la búsqueda en FAISS
    distances, indices = index.search(np.array([query_embedding]), top_k)
    
    # Obtener los fragmentos relevantes basados en los índices
    results = []
    for i in range(top_k):
        idx = indices[0][i]
        if idx != -1:  # Comprobar que el índice sea válido
            result = {
                "movie": metadata[idx]["movie"],
                "fragment_id": metadata[idx]["fragment_id"],
                "text": metadata[idx]["text"],
                "distance": distances[0][i]
            }
            results.append(result)
            print(f"Fragmento encontrado: {result}")
    return results

# Código de prueba
if __name__ == "__main__":
    query = "Describe a tense scene with a lot of suspense."
    results = search_similar_fragments(query, top_k=5)

    # Mostrar los resultados
    for i, result in enumerate(results):
        print(f"\nResultado {i+1}:")
        print(f"Película: {result['movie']}")
        print(f"Fragmento ID: {result['fragment_id']}")
        print(f"Texto del Fragmento: {result['text']}")
        print(f"Distancia: {result['distance']}")
