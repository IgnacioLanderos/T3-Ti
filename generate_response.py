# generate_response.py

import requests
import time
from retrieve_information import search_similar_fragments

# URL de la API del LLM
llm_api_url = "http://tormenta.ing.puc.cl/api/generate"

def get_llm_response(query, context_fragments, retries=2, fragment_limit=1, char_limit=50):
    """
    Envía la consulta y los fragmentos de contexto a la API del LLM y obtiene una respuesta.
    Si la API falla, devuelve una respuesta simulada.
    """
    # Limitación de fragmentos y caracteres para cada uno.
    context_fragments = context_fragments[:fragment_limit]
    context = "\n\n".join([f"{i + 1}. {frag['movie']} (Fragmento {frag['fragment_id']}): {frag['text'][:char_limit]}"
                           for i, frag in enumerate(context_fragments)])

    prompt = (f"Actúa como un asistente de consulta de películas que proporciona respuestas detalladas sobre "
              f"las siguientes películas: Anastasia, Finding Nemo, Despicable Me 2, It, John Wick, Life of Pi, "
              f"Oblivion, The Pianist, Puss in Boots: The Last Wish y Scream.\n\n"
              f"A continuación se muestran fragmentos de una o más de estas películas que pueden servir de contexto "
              f"para responder la pregunta:\n\n"
              f"{context}\n\n"
              f"Pregunta: {query}\n"
              f"Proporciona una respuesta relacionada a la consulta de manera clara y breve")

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "integra-LLM",
        "prompt": prompt,
        "max_tokens": 30,
        "stream": False
    }

    # Intentos de conexión a la API
    for attempt in range(retries):
        try:
            response = requests.post(llm_api_url, headers=headers, json=payload, timeout=300)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "No se pudo generar la respuesta.")
            elif response.status_code == 504:
                print("Timeout de la API, reintentando...")
                time.sleep(5)
            else:
                print(f"Error en la API del LLM: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            print("Excepción de timeout, reintentando...")
            time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    simulated_response = (
        "Esta es una respuesta simulada para ilustrar el funcionamiento del sistema. "
        "Parece que actualmente no podemos obtener una respuesta real de la API, esperar más tarde."
    )
    print("No se pudo obtener una respuesta después de varios intentos. Usando respuesta simulada.")
    return simulated_response

# Código de prueba
if __name__ == "__main__":
    query = "¿Quién es Anastasia?"
    context_fragments = search_similar_fragments(query, top_k=40)

    # Llamada a la función para obtener la respuesta
    response = get_llm_response(query, context_fragments)

    # Mostrar la respuesta generada por el LLM (o simulada si falla)
    print("\nRespuesta del LLM:")
    print(response)
