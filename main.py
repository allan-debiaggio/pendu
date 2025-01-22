import pygame
import requests
import random
import json
import os

# Liste des URLs d'API
api_urls = [
    "https://trouve-mot.fr/api/categorie/6",
    "https://trouve-mot.fr/api/categorie/19",
    "https://trouve-mot.fr/api/categorie/16",
    "https://trouve-mot.fr/api/categorie/17",
    "https://trouve-mot.fr/api/categorie/5",
]

words = []

# Charger les mots existants depuis le fichier JSON s'il existe
json_file_path = 'words.json'
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as file:
        words = json.load(file)

# Fonction pour choisir un mot aléatoire depuis la liste existante
def get_random_word():
    if words:
        return random.choice(words)
    return None

# Tenter de récupérer des mots depuis les APIs
for url in api_urls:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                word = data[0].get('name', None)  # Assurez-vous que 'name' est correct
                if word and word not in words:
                    words.append(word)
            else:
                print(f"Aucune donnée reçue depuis l'API : {url}")
        else:
            print(f"Erreur lors de la requête API ({url}) : {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"Requête API ({url}) a expiré après 10 secondes.")
        break
    except requests.exceptions.ConnectionError as e:
        print(f"Erreur de connexion à l'API. Chargement de la liste locale")
        break
    except Exception as e:
        print(f"Une erreur inattendue est survenue pour l'API ({url}) : {e}")
        break

# Sauvegarder les mots dans le fichier JSON
with open(json_file_path, 'w') as file:
    json.dump(words, file, ensure_ascii=False, indent=4)

# Si aucun mot n'a été choisi, en choisir un aléatoirement depuis la liste locale
selected_word = get_random_word()
if selected_word:
    print(f"Mot choisi aléatoirement depuis la liste locale : {selected_word}")
else:
    print("Aucun mot n'est disponible dans la liste locale.")

pygame.init()
