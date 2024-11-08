# generate_embeddings.py
# Este script genera embeddings para cada fragmento de guion y los almacena en una base de datos vectorial.

import os
import requests
import json

# Carpeta donde están los guiones procesados
input_folder = "scripts"
api_url = "http://tormenta.ing.puc.cl/api/embed"  # URL de la API para generar embeddings

def get_embedding(text):
    """
    Genera el embedding para un fragmento de texto usando la API 'nomic-embed-text'.
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "nomic-embed-text",
        "input": text
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["embeddings"][0]  # Obtener el vector de embedding
    else:
        print(f"Error en la API: {response.status_code}")
        return None

def process_scripts_for_embeddings(input_folder):
    embeddings_data = []
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().split("\n\n---\n\n")  # Separar por fragmentos usando el delimitador
            for i, fragment in enumerate(content):
                fragment = fragment.strip()
                if fragment:  # Evitar fragmentos vacíos
                    embedding = get_embedding(fragment)
                    if embedding:
                        embeddings_data.append({
                            "movie": filename,
                            "fragment_id": i,
                            "embedding": embedding,
                            "text": fragment
                        })
                        print(f"Embedding generado para fragmento {i} de {filename}")
    return embeddings_data

# Generar y almacenar embeddings
embeddings_data = process_scripts_for_embeddings(input_folder)

# Guardar los embeddings en un archivo JSON para almacenamiento temporal
with open("embeddings_data.json", "w", encoding="utf-8") as f:
    json.dump(embeddings_data, f, ensure_ascii=False, indent=4)

print("Embeddings generados y guardados en embeddings_data.json")
