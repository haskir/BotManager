import platform
import time
import asyncio, dotenv, os, time
from asyncio import sleep as asleep
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
import dotenv
import os
from Process import Process

dotenv.load_dotenv()

BOT_MANAGER: str = os.getenv('BOT_MANAGER')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))


def __parse_workers_folder() -> list[str]:
    return list(os.listdir("./Workers/"))


bot: Bot = Bot(token=BOT_MANAGER)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)


# @dp.message(Command(commands=['start_mailing']))
# async def start_mailing(message: Message):
#     if message.from_user.id != ADMIN_ID:
#         await message.answer(text="Только админу разрешено.")
#         return
#     global mailing_enabled
#     if mailing_enabled:
#         await message.answer(text="Рассылка уже была включена ранее")
#         return
#     mailing_enabled = True
#     await message.answer(text=f"Включил рассылку на {goal_time.time()}")
#
#
@dp.message(Command(commands=['show_running_processes']))
async def show_running_processes(message: Message):
    if message.from_user.id != ADMIN_ID:
        print(f"Тут к тебе чел стучался {message.from_user.id}")
        await message.answer(text="Только админу разрешено.")
        return
    await message.answer(text="\n".join([str(proc) for proc in processes.values()]),
                         reply_markup=keyboard_processes.as_markup())

@dp.message()
async def Any(message: Message):
    await message.answer(text="\n".join(processes.keys()))


async def main():
    await dp.start_polling(bot, skip_updates=True)


# Запускаем бота
if __name__ == '__main__':
    for string in __parse_workers_folder():
        print(string)
    if platform.system() == "Windows":
        python_executor = r"venv/Scripts/python.exe"
    else:
        python_executor = r"venv/bin/python3.11"
    exec_path = os.path.abspath('')

    processes = {project: Process(name=project,
                                  exec_path=f"{exec_path}/Workers/{project}/",
                                  python_executor=f"{python_executor}")
                  for project in __parse_workers_folder()}

    from aiogram.utils.keyboard import (InlineKeyboardBuilder, InlineKeyboardButton)
    # subscribe_button = InlineKeyboardButton(text="Подписаться", callback_data="Subscribe")
    # unsubscribe_button = InlineKeyboardButton(text="Отписаться", callback_data="Unsubscribe")
    # more_button = InlineKeyboardButton(text="Пасту хочу", callback_data="More")

    keyboard_processes = InlineKeyboardBuilder()
    keyboard_processes.add(*[InlineKeyboardButton(
        text=pr.name,
        callback_data=pr.name) for pr in processes.values()])
    # {process.start() for process in processes.values()}


    asyncio.run(main())