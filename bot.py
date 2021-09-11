import logging
import os
import png
from pyqrcode import QRCode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
TOKEN = os.environ.get('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
start_msg = '''
<b>Hello Friend,</b> <i>I'm Qr Code Bot.</i>

Send Me any Email ID,Text,any url etc. I will generate a qr code for it.

<b>Direct Media files Are not supported</b>

@TGqrcodebot|@SBS_Studio
'''
help_msg = '''
Send Me any Email ID,Text,any url etc. I will generate a qr code for it.

<b>Direct Media files Are not supported</b>

@TGqrcodebot|@SBS_Studio
'''


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_html(start_msg)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_html(help_msg)


def msg(update: Update, context: CallbackContext) -> None:
    """Send Any text or url to get a qr code for it"""
    text = update.message.text
    message_id = update.message.message_id
    qr_file = f'{message_id}.png'
    try:
        update.message.reply_text("Generating")
        Qr_Code = QRCode(text)
        Qr_Code.png(qr_file, scale=10)
        update.message.reply_photo(photo=open(
            qr_file, "rb"), reply_to_message_id=message_id, caption=f"Here is Your Qr code for '{text}' \n\n@TGqrcodebot|@SBS_Studio")
        update.message.reply_text("Finished")
        os.remove(qr_file)
    except Exception:
        update.message.reply_text("Please Try Agian Later")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, msg))
    # Start The bot
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
