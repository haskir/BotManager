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
from Keyboards import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
dotenv.load_dotenv()
BOT_MANAGER: str = os.getenv('BOT_MANAGER')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))


def __parse_workers_folder() -> list[str]:
    return list(os.listdir("./Workers/"))


bot: Bot = Bot(token=BOT_MANAGER)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)


@dp.message(lambda mes: mes.from_user.id != ADMIN_ID)
async def not_admin(message: Message):
    await message.answer(text="Тебе здесь не рады")


@dp.callback_query(lambda call: call.from_user.id != ADMIN_ID)
async def not_admin(message: Message):
    await message.answer(text="Тебе здесь не рады")


@dp.message(Command(commands=['show_running_processes']))
async def show_running_processes(message: Message):
    text = 'Processes:\n' + "\n".join(str(proc) for proc in processes.values() if proc.error_notification)
    await message.answer(text=text,
                         reply_markup=keyboard_processes.as_markup())


@dp.callback_query(lambda call: call.data in __parse_workers_folder())
async def select_process(callback: CallbackQuery):
    await callback.message.answer(text=f'{callback.data}',
                                  reply_markup=keyboards[callback.data].as_markup())


@dp.callback_query(lambda call: "$" in call.data)
async def action_with_selected_process(callback: CallbackQuery):
    process, action = callback.data.split("$")
    try:
        class_method = getattr(processes[process], action)
        await callback.message.answer(
            text=class_method()
        )
    except Exception as e:
        print(e)


@dp.message()
async def Any(message: Message):
    await message.answer(text="\n".join(processes.keys()))


@dp.callback_query(lambda call: "back" in call.data)
async def back(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        print(f"Тут к тебе чел стучался {callback.message.from_user.id}")
        await callback.message.answer(text="Только админу разрешено.")
        return
    await callback.message.answer(text=f'Processes:',
                                  reply_markup=keyboard_processes.as_markup())


@dp.callback_query()
async def Any(callback: CallbackQuery):
    print(callback.data)


async def stopped_checker():
    for proc in processes.values():
        if "stopped" in str(proc):
            await bot.send_message(text=proc.name + " is stopped",
                                   chat_id=ADMIN_ID)


def on_startup():
    scheduler.add_job(stopped_checker, "cron", minute="*/15", jitter=120)
    scheduler.start()


async def main():
    await dp.start_polling(bot, skip_updates=True, on_startup=on_startup())


# Запускаем бота
if __name__ == '__main__':
    if platform.system() == "Windows":
        python_executor = r"venv/Scripts/python.exe"
    else:
        python_executor = r"venv/bin/python3.11"
    exec_path = os.path.abspath('')

    processes = {project: Process(name=project,
                                  exec_path=f"{exec_path}/Workers/{project}/",
                                  python_executor=f"{python_executor}")
                 for project in __parse_workers_folder()}

    keyboard_processes = InlineKeyboardBuilder()
    for process in processes.values():
        keyboard_processes.row(
            InlineKeyboardButton(
                text=process.name,
                callback_data=process.name))

    # {process.start() for process in processes.values()}

    asyncio.run(main())
