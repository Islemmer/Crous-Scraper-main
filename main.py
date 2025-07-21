import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Setup logging for Railway
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise EnvironmentError("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in environment variables.")

# URL for Lyon
URL = "https://trouverunlogement.lescrous.fr/tools/41/search"

# Set of seen results to avoid duplicates
seen = set()

# Scraping function
def get_logements():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Request error: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="fr-card svelte-12dfls6")

    logements = []
    for card in cards:
        title = card.find("h3")
        if title:
            logements.append(title.text.strip())
    return logements

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot is up and running!")

# Command /scrape to trigger scraping manually
async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("🔍 Manual /scrape triggered.")
    logements = get_logements()
    new_logements = [log for log in logements if log not in seen]

    if new_logements:
        for logement in new_logements:
            seen.add(logement)
            await update.message.reply_text(f"🏠 Nouveau logement à Lyon : {logement}")
    else:
        await update.message.reply_text("😴 Aucun nouveau logement pour le moment.")

# Main function
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("scrape", scrape))

    # Start bot
    logging.info("🤖 Bot started via webhook/polling.")
    application.run_polling()

if __name__ == "__main__":
    main()
