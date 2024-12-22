import json
import telebot
from datetime import datetime
import logging
import os
import sys
import time
import requests
from requests.exceptions import ReadTimeout

# Load the devices.json data
with open("devices.json") as f:
    devices_data = json.load(f)

# Example of accessing the database details (e.g., BlazeVersion)
database = {
    'BlazeVersion': 'v4.1'
}

# Telegram Bot Token and Chat ID
bot_token = '7826621760:AAEX6C-U1D_1V6kw04DxC662Mllaw-iWgvY'
chat_id = '-1001502290877'
admin_id = '1024560836'  # Your provided admin user ID

# Initialize the bot
bot = telebot.TeleBot(bot_token)

# Set up logging to output to the server screen (console)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout  # Output logs to standard output
)
logger = logging.getLogger()

# Function to escape HTML special characters
def escape_html(text):
    """
    Escapes HTML special characters for safety.
    """
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
    post_date = datetime.now().strftime("%b-%d-%Y")  # e.g., Nov-26-2024
    
    # Escape the details for HTML safety
    device = escape_html(device)
    codename = escape_html(codename)
    maintainer = escape_html(maintainer)
    sgroup = escape_html(sgroup)

    post = f"""
#Blaze #{codename} #Android15
<strong>Project Blaze {database['BlazeVersion']} - OFFICIAL | Android 15
📲 : {device} ({codename}) 
📅 : {post_date} 
🧑‍💼 : @{maintainer}</strong>

▪️ Changelog: <a href="https://raw.githubusercontent.com/ProjectBlaze/official_devices/refs/heads/14/device/{codename}.txt">Device</a>
▪️ <a href="https://www.projectblaze.in/">Download</a>
▪️ <a href="https://t.me/projectblaze/127505">Screenshots</a>
▪️ <a href="{sgroup}">Support Group</a>
▪️ <a href="https://t.me/projectblaze">Community Chat</a>
▪️ <a href="https://t.me/projectblazeupdates">Updates Channel</a>

#VanillaIceCream #Stable #Reborn
"""
    return post

# Function to ensure that the webhook is deleted before starting polling
def delete_webhook():
    try:
        bot.remove_webhook()  # This will delete the active webhook
        logger.info("Webhook successfully removed.")
    except Exception as e:
        logger.error(f"Error while removing webhook: {e}")
        bot.send_message(admin_id, f"Error while removing webhook: {e}")

# Command handler for /post
@bot.message_handler(commands=['post'])
def handle_post_command(message):
    try:
        # Log the incoming command
        logger.info(f"Received /post command from {message.from_user.username} with args: {message.text}")
        
        # Check if the message contains a codename
        if len(message.text.split()) > 1:
            codename = message.text.split()[1]
            post_content = create_post(codename)
            
            # If codename is not found in the devices data
            if "not found" in post_content:
                bot.reply_to(message, post_content)
                logger.warning(f"Codename {codename} not found. No image sent.")
            else:
                # Path to the fixed image
                image_path = "banner/blaze_4.1.png"

                if os.path.exists(image_path):
                    # Send the fixed image along with the post content
                    with open(image_path, 'rb') as image_file:
                        bot.send_photo(chat_id, image_file, caption=post_content, parse_mode='HTML')
                    
                    # Send confirmation to the user
                    bot.reply_to(message, f"Post for codename {codename} has been successfully created!")
                    
                    # Log successful post
                    logger.info(f"Successfully posted for codename: {codename}")
                else:
                    bot.reply_to(message, "Image blaze_4.1.png not found in the banner folder.")
                    logger.warning("Image blaze_4.1.png not found in the banner folder.")
        else:
            bot.reply_to(message, "Please provide the codename of the device after the /post command.")
            logger.warning(f"Invalid /post command received: No codename provided.")
    except Exception as e:
        logger.error(f"Error while processing /post command: {e}")
        bot.reply_to(message, "An error occurred while processing your request.")
        logger.exception("Exception traceback:")

        # Notify the admin about the error
        bot.send_message(admin_id, f"Error occurred while processing /post command: {e}")
        bot.send_message(admin_id, f"Traceback:\n{str(e)}")

# Start the bot with webhook deletion before polling
if __name__ == "__main__":
    try:
        # Ensure the webhook is removed
        delete_webhook()

        # Log that the bot is starting
        logger.info("Bot is starting...")

        # Send a startup message to admin
        bot.send_message(admin_id, "Bot is starting...")

        # Start polling with timeout handling
        while True:
            try:
                bot.polling(none_stop=True, interval=1, timeout=60, long_polling_timeout=60)
            except ReadTimeout:
                logger.warning("Read timeout occurred. Retrying...")
                bot.send_message(admin_id, "A read timeout occurred. Bot is retrying...")
                time.sleep(5)  # Wait before retrying
            except Exception as e:
                logger.error(f"Unexpected error in polling: {e}")
                bot.send_message(admin_id, f"Unexpected error occurred: {e}")
                logger.exception("Exception traceback:")
                time.sleep(10)  # Wait before retrying in case of unexpected errors
    except Exception as e:
        logger.error(f"Error while starting the bot: {e}")
        bot.send_message(admin_id, f"Bot failed to start: {e}")
        logger.exception("Exception traceback:")
