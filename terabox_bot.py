import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Telegram Bot Token
TELEGRAM_TOKEN = '7482295980:AAGWb2AdTGIqFIfi0cQdvJHoxmh1Y-Rj2pY'

# Mock TeraBox credentials (you will need to fill these with actual data)
TERABOX_USERNAME = 'b13titan.01@gmail.com'
TERABOX_PASSWORD = 'Laxmijb12'

def start(update, context):
    update.message.reply_text("Hi! Send me a file and I'll upload it to TeraBox for you.")

def login_to_terabox():
    # This is a placeholder. Replace with actual login functionality
    # that returns a session or token
    session = requests.Session()
    # Perform login with session here
    return session

def upload_file_to_terabox(session, file_path):
    # Replace this URL and logic with the correct TeraBox upload endpoint
    upload_url = 'https://www.terabox.com/api/upload'
    
    with open(file_path, 'rb') as f:
        response = session.post(upload_url, files={'file': f})
        return response.json()

def handle_document(update, context):
    # Download the file sent to the bot
    file = update.message.document.get_file()
    file_path = file.download()
    
    update.message.reply_text('Uploading your file to TeraBox...')

    # Log in to TeraBox and upload the file
    session = login_to_terabox()
    if not session:
        update.message.reply_text('Failed to log in to TeraBox.')
        return
    
    result = upload_file_to_terabox(session, file_path)
    update.message.reply_text(f'File uploaded! Response: {result}')

    # Clean up the downloaded file
    os.remove(file_path)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
