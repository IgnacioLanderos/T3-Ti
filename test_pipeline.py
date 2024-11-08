# test_pipeline.py
# Este script prueba el flujo completo desde la consulta hasta la respuesta generada por el LLM.

from retrieve_information import search_similar_fragments
from generate_response import get_llm_response

def run_test(query):
    print(f"Consulta del usuario: {query}")

    # Paso 1: Buscar fragmentos relevantes
    print("\nBuscando fragmentos relevantes...")
    context_fragments = search_similar_fragments(query, top_k=5)

    if not context_fragments:
        print("No se encontraron fragmentos relevantes.")
        return

    print("\nFragmentos encontrados:")
    for i, fragment in enumerate(context_fragments):
        print(f"\nFragmento {i+1} (de {fragment['movie']}):")
        print(fragment["text"])

    # Paso 2: Generar respuesta con el LLM
    print("\nGenerando respuesta...")
    response = get_llm_response(query, context_fragments)

    if response:
        print("\nRespuesta del LLM:")
        print(response)
    else:
        print("No se pudo generar una respuesta.")

# Ejemplo de consulta para probar el flujo completo
query = "Describe a tense scene with a lot of suspense."
run_test(query)
