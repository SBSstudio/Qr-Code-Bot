import logging
import os
import png
from pyqrcode import QRCode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import ffmpeg
import uuid
import math
import asyncio
import logging
import threading
import unittest, time, datetime
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from pyrogram import Client, filters
from asyncio import get_running_loop
from functools import partial
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
import shutil

TOKEN = os.environ.get('TOKEN')
UPDTE_CHNL = os.environ.get('UPDTE_CHNL')

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

        
async def pyro_fsub(c, message, fsub):
    try:
        user = await c.get_chat_member(fsub, message.chat.id)
        if user.status == "kicked":
            await c.send_message(
                chat_id=message.chat.id,
                text="Sorry, You are Banned to use me.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
        return True
    except UserNotParticipant:
        chnl = os.environ.get("UPDTE_CHNL")
        await c.send_message(
            chat_id=message.chat.id,
            text="**Please Join My Updates Channel to Use Me!**",
        return False
    except Exception as kk:
        print(kk)
        await c.send_message(
            chat_id=message.chat.id,
            text="Something went Wrong.",
            parse_mode="markdown",
            disable_web_page_preview=True)
        return False
    
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
