import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Command handler for /start and /help
@dp.message(Command("start", "help"))
async def command_start_handler(message: Message):
    """
    Handles /start and /help commands
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by Aiogram 3.x.")

# Echo handler for all messages
@dp.message()
async def echo(message: Message):
    """
    Echo back the received message
    """
    await message.answer(message.text)

# Main function to start the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

