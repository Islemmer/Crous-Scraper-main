import os
import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot
import logging

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not TOKEN or not CHAT_ID:
    raise EnvironmentError("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in environment variables.")
bot = Bot(token=TOKEN)

# First startup message
bot.send_message(chat_id=CHAT_ID, text="✅ Bot Railway lancé avec succès ! Surveillance des logements activée.")

# --- Location URLs with names ---
URLS = {
    "Lyon (global)": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.8583622_45.7955875_4.9212614_45.7484524",
    "Bron": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.8867336_45.7529223_4.9365026_45.7179904",
    "Vénissieux": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.849741_45.7307049_4.9112904_45.6716156",
    "Villeurbanne (Polytech Lyon)": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.867751_45.779573_4.868567_45.779163",
    "Université Claude Bernard - Lyon 1 , Villeurbanne": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.864781_45.787349_4.8854094_45.7790127",
    "Institut National des Sciences Appliquées de Lyon, Villeurbanne": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.8707876_45.7870507_4.884328_45.7792446", 
}

# Seen listings per location
seen_logements = {name: set() for name in URLS}

# --- Scraping Function ---
def get_logements(url):
    try:
        response = requests.get(url)
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

# --- Main Loop ---
def main_loop():
    while True:
        for name, url in URLS.items():
            logging.info(f"🔍 Vérification des logements pour : {name}")
            logements = get_logements(url)
            logging.info(f"📦 {len(logements)} logements trouvés à {name}.")

            new_logements = [log for log in logements if log not in seen_logements[name]]

            if new_logements:
                logging.info(f"🚨 {len(new_logements)} nouveau(x) logement(s) à {name} !")
                for logement in new_logements:
                    message = f"🏠 Nouveau logement à {name} : {logement}"
                    try:
                        bot.send_message(chat_id=CHAT_ID, text=message)
                        seen_logements[name].add(logement)
                    except Exception as e:
                        logging.warning(f"⚠️ Erreur envoi Telegram : {e}")
            else:
                logging.info(f"🕒 Aucun nouveau logement à {name}.")

        time.sleep(30)  # Adjust this interval if needed (e.g., 120 for 2 minutes)

# --- Run ---
if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info("🛑 Script arrêté manuellement.")
