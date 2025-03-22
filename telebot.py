import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import openai

class Reference:
    '''
    A class to store previously generated responses from the ChatGPT API
    '''
    def __init__(self) -> None:
        self.response = ""

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Model name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher (Correct way in Aiogram v3)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher()

def clear_past():
    """A function to clear the previous conversation and context."""
    reference.response = ""

# Register handlers using `@dispatcher.message(Command("command_name"))`
@dispatcher.message(Command("start"))
async def welcome(message: Message):
    """
    This handler responds to the `/start` command.
    """
    await message.answer("Hi\nI am Tele Bot!\nCreated by Urvi Thakur. How can I assist you?")

@dispatcher.message(Command("clear"))
async def clear(message: Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.answer("I've cleared the past conversation and context.")

@dispatcher.message(Command("help"))
async def helper(message: Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm ChatGPT Telegram bot created by Urvi Thakur! Please follow these commands:
    
    /start - Start the conversation
    /clear - Clear past conversation and context
    /help - Show this help menu
    
    I hope this helps. :)
    """
    await message.answer(help_command)

@dispatcher.message()
async def chatgpt(message: Message):
    """
    A handler to process the user's input and generate a response using the ChatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},  # Previous response
            {"role": "user", "content": message.text}  # User query
        ]
    )
    reference.response = response["choices"][0]["message"]["content"]
    print(f">>> ChatGPT: \n\t{reference.response}")
    await message.answer(reference.response)

async def main():
    """Start the bot using async event loop"""
    logging.basicConfig(level=logging.INFO)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
