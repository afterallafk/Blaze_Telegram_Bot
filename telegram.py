import json
import os
import logging
import requests
from datetime import datetime
from telegram import Bot
from telegram.ext import CommandHandler, Updater, Dispatcher, MessageHandler, Filters
from logging.handlers import RotatingFileHandler

# Bot token and chat ID
bot_token = '7826621760:AAEX6C-U1D_1V6kw04DxC662Mllaw-iWgvY'
chat_id = '-1001502290877'

# Initialize bot and logger
bot = Bot(bot_token)

# Set up logging with rotation
log_handler = RotatingFileHandler("bot_logs.log", maxBytes=5*1024*1024, backupCount=3)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def escape_html(text):
    html_escapes = {
        '&': '&amp;',
        '"': '&quot;',
        "'": '&#x27;',
        '>': '&gt;',
        '<': '&lt;',
        '/': '&#x2F;'
    }
    return ''.join(html_escapes.get(c, c) for c in text)

def create_post(codename):
    # Find the device matching the given codename
    device_info = next((device for device in devices_data if device['codename'] == codename), None)
    
    if not device_info:
        return f"Device with codename {codename} not found."
    
    device = device_info['device']
    maintainer = device_info['maintainer']
    sgroup = device_info['sgroup']
    post_date = datetime.now().strftime("%b-%d-%Y")
    
    # Escape the details for HTML safety
    device = escape_html(device)
    codename = escape_html(codename)
    maintainer = escape_html(maintainer)
    sgroup = escape_html(sgroup)

    post = f"""
#Blaze #{codename} #Android15 #VanillaIceCream #Stable
<strong>Project Blaze {database['BlazeVersion']}-BETA - OFFICIAL | Android 15</strong>
📲 : {device} ({codename}) 
📅 : {post_date} 
🧑‍💼 : @{maintainer}

▪️ Changelog: <a href="https://raw.githubusercontent.com/ProjectBlaze/official_devices/refs/heads/14/device/{codename}.txt">Device</a>
▪️ <a href="https://www.projectblaze.in/">Download</a>
▪️ <a href="https://t.me/projectblaze/120561">Screenshots</a>
▪️ <a href="https://t.me/{sgroup}">Support Group</a>
▪️ <a href="https://t.me/projectblaze">Community Chat</a>
▪️ <a href="https://t.me/projectblazeupdates">Updates Channel</a>
"""
    
    return post

def handle_post_command(update, context):
    try:
        message = update.message
        if len(message.text.split()) > 1:
            codename = message.text.split()[1]
            post_content = create_post(codename)
            
            # Send the post content to Telegram chat
            bot.send_message(chat_id, post_content, parse_mode='HTML')
            update.message.reply_text(f"Post for codename {codename} has been successfully created!")
        else:
            update.message.reply_text("Please provide the codename of the device after the /post command.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        update.message.reply_text("An error occurred while processing your request.")
        bot.send_message(admin_id, f"Error: {str(e)}")

def webhook(request):
    if request.method == "POST":
        payload = request.get_json()
        bot = Bot(bot_token)
        updater = Updater(bot=bot)
        dispatcher = updater.dispatcher

        # Handle the '/post' command
        dispatcher.add_handler(CommandHandler("post", handle_post_command))

        # Dispatch the updates to handlers
        dispatcher.process_update(payload)
        return "OK", 200
    return "Method not allowed", 405
