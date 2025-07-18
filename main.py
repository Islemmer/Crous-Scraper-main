import os
import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot

# Lire les variables d’environnement (à définir dans Render)
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

bot = Bot(token=TOKEN)

# URL filtrée pour Lyon uniquement
URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.7718134_45.8082628_4.8983774_45.7073666"

# Stocker les logements déjà vus
seen = set()

def get_logements():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="fr-card svelte-12dfls6")

    logements = []
    for card in cards:
        title = card.find("h3")
        if title:
            logements.append(title.text.strip())
    return logements

# Boucle principale
while True:
    print("🔍 Vérification des nouveaux logements à Lyon...")
    logements = get_logements()
    print(f"📦 {len(logements)} logements trouvés.")

    new_logements = [log for log in logements if log not in seen]

    for log in logements:
        print("➡️", log)

    if new_logements:
        print(f"🚨 {len(new_logements)} nouveau(x) logement(s) trouvé(s) à Lyon !")
        for logement in new_logements:
            message = f"🏠 Nouveau logement à Lyon : {logement}"
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                seen.add(logement)
            except Exception as e:
                print(f"⚠️ Erreur lors de l'envoi du message : {e}")
    else:
        print("🕒 Aucun nouveau logement trouvé.")

    time.sleep(120)  # Attendre 2 minutes
