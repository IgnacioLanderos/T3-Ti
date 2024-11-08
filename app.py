# app.py
# Este script crea una API en Flask que interactúa con el backend para generar respuestas basadas en guiones.

from flask import Flask, request, jsonify, render_template
from retrieve_information import search_similar_fragments
from generate_response import get_llm_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate_response", methods=["POST"])
def generate_response():
    data = request.get_json()
    query = data.get("query", "")
    
    if not query:
        return jsonify({"error": "No se proporcionó ninguna consulta."}), 400
    
    context_fragments = search_similar_fragments(query, top_k=3)
    response = get_llm_response(query, context_fragments)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

