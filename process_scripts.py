# process_scripts.py
# Este script limpia y procesa los guiones descargados y los divide en fragmentos.

import os
import re

input_folder = "scripts"
output_folder = "processed_scripts"
fragment_size = 3000  # Número aproximado de caracteres por fragmento (ajusta según sea necesario)

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

def clean_text(text):
    """
    Limpia el texto eliminando caracteres especiales y espacios extra.
    """
    # Eliminar líneas vacías o con espacios en blanco
    text = re.sub(r'\s*\n\s*', '\n', text)
    # Eliminar caracteres especiales y mantener solo caracteres útiles
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Eliminar caracteres no ASCII
    return text.strip()

def split_into_fragments(text, size):
    """
    Divide el texto en fragmentos de tamaño aproximado especificado.
    """
    fragments = []
    start = 0
    while start < len(text):
        end = start + size
        # Asegura que los fragmentos no terminen a la mitad de una oración.
        if end < len(text):
            end = text.rfind('.', start, end) + 1 or end
        fragments.append(text[start:end].strip())
        start = end
    return fragments

def process_script(file_path, output_folder):
    """
    Procesa un guion, limpiando y dividiendo en fragmentos.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Limpiar el texto
    cleaned_text = clean_text(text)
    
    # Dividir en fragmentos
    fragments = split_into_fragments(cleaned_text, fragment_size)
    
    # Guardar cada fragmento en la carpeta de salida
    output_path = os.path.join(output_folder, os.path.basename(file_path))
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for fragment in fragments:
            output_file.write(fragment + "\n\n---\n\n")  # Separador de fragmentos

    print(f"Guion procesado y guardado en: {output_path}")

# Procesar cada archivo en la carpeta de entrada
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    process_script(file_path, output_folder)
