import os
import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot
import logging

# Logging for Railway logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Lire les variables d’environnement
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise EnvironmentError("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in environment variables.")

bot = Bot(token=TOKEN)

bot.send_message(chat_id=CHAT_ID, text="Hello from Railway!")

# URL filtrée pour Lyon uniquement
URL = "https://trouverunlogement.lescrous.fr/tools/41/search"

# Stocker les logements déjà vus
seen = set()

def get_logements():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erreur lors de la requête : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="fr-card svelte-12dfls6")

    logements = []
    for card in cards:
        title = card.find("h3")
        if title:
            logements.append(title.text.strip())
    return logements

def main_loop():
    while True:
        logging.info("🔍 Vérification des nouveaux logements à Lyon...")
        logements = get_logements()
        logging.info(f"📦 {len(logements)} logements trouvés.")

        new_logements = [log for log in logements if log not in seen]

        if new_logements:
            logging.info(f"🚨 {len(new_logements)} nouveau(x) logement(s) trouvé(s) à Lyon !")
            for logement in new_logements:
                message = f"🏠 Nouveau logement à Lyon : {logement}"
                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    seen.add(logement)
                except Exception as e:
                    logging.warning(f"⚠️ Erreur lors de l'envoi du message : {e}")
        else:
            logging.info("🕒 Aucun nouveau logement trouvé.")

        time.sleep(120)  # Attendre 2 minutes

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info("🛑 Arrêt manuel du script.")
