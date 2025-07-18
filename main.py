import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot

# Lire le token Telegram depuis token.txt
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

# Lire le chat_id Telegram depuis chat_id.txt
with open("chat_id.txt", "r") as f:
    CHAT_ID = f.read().strip()

bot = Bot(token=TOKEN)

# URL filtrée pour Lyon uniquement
URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.7718134_45.8082628_4.8983774_45.7073666"

# Stocker les logements déjà vus
seen = set()

def get_logements():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="fr-card svelte-12dfls6")

    logements = []
    for card in cards:
        title = card.find("h3")
        if title:
            logements.append(title.text.strip())
    return logements

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
            bot.send_message(chat_id=CHAT_ID, text=message)
            seen.add(logement)
    else:
        print("🕒 Aucun nouveau logement trouvé.")

    time.sleep(120)  # Attendre 2 minutes
