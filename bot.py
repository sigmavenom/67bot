import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

user_history = {}


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я Gemini-бот. Напиши мне сообщение."
    )


@dp.message()
async def chat(message: Message):
    user_id = message.from_user.id

    history = user_history.get(user_id, [])

    history.append(
        {
            "role": "user",
            "parts": [message.text]
        }
    )

    try:
        response = model.generate_content(
            history
        )

        answer = response.text

        history.append(
            {
                "role": "model",
                "parts": [answer]
            }
        )

        user_history[user_id] = history[-20:]

        await message.answer(answer)

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())