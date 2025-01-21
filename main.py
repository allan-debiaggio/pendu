import pygame
import requests
import random

api_urls = [ #API URLs
    "https://trouve-mot.fr/api/categorie/6",
    "https://trouve-mot.fr/api/categorie/19",
    "https://trouve-mot.fr/api/categorie/16",
    "https://trouve-mot.fr/api/categorie/17",
    "https://trouve-mot.fr/api/categorie/5",
]

words = []

for url in api_urls:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            word = data[0].get('name', None)  
            if word:
                words.append(word)
        else:
            print(f"Aucune donnée reçue depuis l'API : {url}")
    else:
        print(f"Erreur lors de la requête API ({url}) : {response.status_code}")

if words:
    selected_word = random.choice(words)
    print(f"Mot choisi aléatoirement : {selected_word}")
else:
    selected_word = None
    print("Aucun mot n'a été récupéré des APIs.")



pygame.init()
