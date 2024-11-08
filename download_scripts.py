# download_scripts.py
# Este script descarga los guiones de las películas desde IMSDB y los guarda como archivos de texto.

import requests
from bs4 import BeautifulSoup
import os

# Lista de películas y URLs
movies = {
    "Anastasia": "https://imsdb.com/scripts/Anastasia.html",
    "Finding_Nemo": "https://imsdb.com/scripts/Finding-Nemo.html",
    "Despicable_Me_2": "https://imsdb.com/scripts/Despicable-Me-2.html",
    "It": "https://imsdb.com/scripts/It.html",
    "John_Wick": "https://imsdb.com/scripts/John-Wick.html",
    "Life_of_Pi": "https://imsdb.com/scripts/Life-of-Pi.html",
    "Oblivion": "https://imsdb.com/scripts/Oblivion.html",
    "The_Pianist": "https://imsdb.com/scripts/Pianist,-The.html",
    "Puss_in_Boots": "https://imsdb.com/scripts/Puss-in-Boots-The-Last-Wish.html",
    "Scream": "https://imsdb.com/scripts/Scream.html"
}

# Crear la carpeta de salida si no existe
output_folder = "scripts"
os.makedirs(output_folder, exist_ok=True)

def download_script(movie_name, url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_content = soup.find('pre')  # Buscar el contenido del guion en la etiqueta <pre>
        
        if script_content:
            script_text = script_content.get_text()
            file_path = os.path.join(output_folder, f"{movie_name}.txt")
            
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(script_text)
            
            print(f"Guion de '{movie_name}' guardado en {file_path}")
        else:
            print(f"No se encontró contenido de guion para '{movie_name}' en {url}")
    else:
        print(f"Error al acceder a {url} (Código: {response.status_code})")

# Descargar cada guion
for movie, url in movies.items():
    download_script(movie, url)
