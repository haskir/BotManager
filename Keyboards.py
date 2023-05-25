from aiogram.utils.keyboard import (InlineKeyboardBuilder, InlineKeyboardButton)
import platform
import time
import asyncio, dotenv, os, time
from asyncio import sleep as asleep
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message


workers = list(os.listdir("./Workers/"))
keyboards = {worker: InlineKeyboardBuilder() for worker in workers}

for worker in keyboards:
    print(worker)

    start_button = InlineKeyboardButton(text="start", callback_data=f"{worker}$start")
    stop_button = InlineKeyboardButton(text="stop", callback_data=f"{worker}$stop")
    status_button = InlineKeyboardButton(text="status", callback_data=f"{worker}$status")
    update_button = InlineKeyboardButton(text="update", callback_data=f"{worker}$update")
    log_button = InlineKeyboardButton(text="log", callback_data=f"{worker}$log")
    error_log_button = InlineKeyboardButton(text="error_log", callback_data=f"{worker}$error_log")
    back_button = InlineKeyboardButton(text="back", callback_data=f"back")

    keyboards[worker].row(start_button, stop_button, status_button)
    keyboards[worker].row(update_button, log_button, error_log_button)
    keyboards[worker].row(back_button)