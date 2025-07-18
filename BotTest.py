from telegram import Bot

BOT_TOKEN = "8079241011:AAE77c5eBzfdQSkYqwTCl3pdzI8KSdCusqg"
CHAT_ID = "5976557506"

bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text="✅ Test message depuis VS Code.")
