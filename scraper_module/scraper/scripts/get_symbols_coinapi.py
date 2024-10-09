import requests
import json
import time

# URL de l'API CoinAPI
url = 'https://rest.coinapi.io/v1/symbols'

# Clé API
api_key = '0EF304A1-6778-4088-A8CC-5418286CD93A'

# En-têtes avec clé API
headers = {
    'X-CoinAPI-Key': api_key
}

# Effectuer la requête HTTP avec le streaming activé
try:
    print("Envoi de la requête à CoinAPI...")

    # Envoyer la requête avec une gestion du temps d'attente (timeout)
    response = requests.get(url, headers=headers, stream=True, timeout=(10, 60))  # timeout: (conn. timeout, read timeout)

    # Vérifier si la requête a réussi
    response.raise_for_status()

    # Créer un fichier JSON pour enregistrer les données
    with open('coinapi_symbols.json', 'w') as json_file:
        print("Téléchargement et écriture des données dans le fichier JSON...")

        # Lire et écrire la réponse en streaming
        for chunk in response.iter_content(chunk_size=1024):  # Traiter des blocs de 1KB
            if chunk:
                json_file.write(chunk.decode('utf-8'))  # Décoder le contenu et écrire dans le fichier

    print("Données enregistrées avec succès dans coinapi_symbols.json")

except requests.exceptions.Timeout:
    print("La requête a dépassé le temps d'attente.")
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de la requête: {e}")
