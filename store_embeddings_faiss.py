# store_embeddings_faiss.py
# Este script carga los embeddings desde embeddings_data.json y los almacena en FAISS para realizar búsquedas.

import faiss
import numpy as np
import json

# Cargar los embeddings desde el archivo JSON
with open("embeddings_data.json", "r", encoding="utf-8") as f:
    embeddings_data = json.load(f)

# Extraer los embeddings y prepararlos para FAISS
dimension = 768  # Dimensionalidad de los embeddings
index = faiss.IndexFlatL2(dimension)  # Índice para búsquedas de similitud

# Lista para almacenar metadatos
metadata = []

for data in embeddings_data:
    embedding = np.array(data["embedding"]).astype("float32")
    index.add(np.array([embedding]))  # Añadir el embedding al índice de FAISS
    metadata.append({
        "movie": data["movie"],
        "fragment_id": data["fragment_id"],
        "text": data["text"]
    })

# Guardar el índice FAISS y los metadatos
faiss.write_index(index, "movie_scripts.index")
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=4)

print("Embeddings almacenados en FAISS y metadatos guardados en metadata.json")
