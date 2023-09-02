import os
import telebot
from decouple import config

# Load Telegram bot values from .env file
telegram_token = config('TELEGRAMTOKEN')
telegram_chat_id = config('TELEGRAMCHATID')

def clear_wordlist():
    with open("./database/wordlist.txt", "w") as file:
        file.truncate(0)
        print("[INFO] Clearing Wordlist")

def clear_hits():
    with open("./database/hits.txt", "w") as file:
        file.truncate(0)
        print("[INFO] Clearing Hits")

# Initialize the Telegram bot
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🦀 Send me a wordlist.")
    print("[INFO] Asking for wordlist.")

@bot.message_handler(func=lambda message: True)
def save_to_wordlist(message):
    clear_wordlist()
    clear_hits()
    user_input = message.text
    with open("./database/wordlist.txt", "a") as file:
        file.write(user_input + "\n")
    bot.reply_to(message, "🦀 Saving Content to DB...")
    print("[ACTION] Saving Content to DB...")

    # Run checker.py using os.system
    print("[SUBPROCESS] Running Checker...")
    os.system('python3 ./logic/checker.py')

bot.polling()