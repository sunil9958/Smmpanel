import telebot
import requests

# Telegram Bot Token
BOT_TOKEN = "8110754193:AAE7OW5xiG4uwl9EfbyQ1Sx73PT3GauE9Ls"

# SMM Panel API Details
SMM_API_URL = "https://indiansmartpanel.com/api"
SMM_API_KEY = "c893ed33cfc5989096919c9fe069a3d88cfca13d"

bot = telebot.TeleBot(BOT_TOKEN)

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome! Send your Instagram username:")

# Handle Instagram Username
@bot.message_handler(func=lambda message: True)
def handle_username(message):
    username = message.text
    bot.send_message(message.chat.id, "Enter the number of followers you want:")
    
    bot.register_next_step_handler(message, lambda m: process_order(m, username))

# Order Processing
def process_order(message, username):
    try:
        quantity = int(message.text)
        
        # Define service ID from your SMM panel (replace with correct service ID)
        service_id = 1297  # Example: Facebook video views service, replace with correct one
        
        # Order Data
        data = {
            "key": SMM_API_KEY,
            "action": "add",
            "service": service_id,
            "link": f"https://www.instagram.com/{username}",
            "quantity": quantity
        }
        
        # Place Order
        response = requests.post(SMM_API_URL, data=data)
        result = response.json()
        
        if "order" in result:
            bot.send_message(message.chat.id, f"Order placed successfully! Order ID: {result['order']}")
        else:
            bot.send_message(message.chat.id, f"Failed to place order. Error: {result}")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid quantity! Please enter a number.")

# Start the bot
bot.polling()
