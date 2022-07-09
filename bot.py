from io import BytesIO
import json
import os
import time
import sys
import logging
import re

import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import exceptions
from aiogram.utils.exceptions import Throttled

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
from utils.files import download_to_bytes
from utils.logger import setup_logger
from utils.messages import send_message_safe, send_media_safe, broadcast_message
from filters import setup_filters, IsAdmin, IsNotCommand
from handlers import init_default_handlers
from states import UserStates, not_processing_state
from keyboards import KEYBOARDS

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--test", help="Use test bot instance", dest='test', action='store_true')
parser.set_defaults(test=False)
args = parser.parse_args()


# init storage and bot
storage = MemoryStorage()
API_KEY = config.test_api_key if args.test else config.api_key
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=storage)

# setup filters
setup_filters(dp)

# setup default handlers
init_default_handlers(dp)

#
@dp.errors_handler()
async def global_error_handler(update, exception):
    logger.error(f'Update: {update} \n{exception}', exc_info=True)
    
    
async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("Please, don't spam!")
#
    

@dp.message_handler(state=not_processing_state, commands=['start'])
@dp.throttled(anti_flood, rate=2)
async def start_message(message: types.Message, state: FSMContext):
    await UserStates.start.set()
    await message.answer(
        "Example start message. Send me any image",
        reply_markup=KEYBOARDS['hide']
    )

    
@dp.message_handler(state='*', commands=['help'])
@dp.throttled(anti_flood, rate=2)
async def help_message(message: types.Message, state: FSMContext):
    await message.answer(
        "Example help message"
    )

    
# example of how to work with images
@dp.message_handler(state=[UserStates.start, None], content_types=['photo'])
@dp.throttled(anti_flood, rate=2)
async def reply_image(message: types.Message, state: FSMContext):     
    if message.photo is not None and len(message.photo) > 0:
        file_url = await message.photo[-1].get_url()
        filename = 'example.png'
    else:
        await message.answer(
            "Can't recognize your attached photo"
        )
        return
    
    image_bytes = await download_to_bytes(file_url) 
    image_bytes.name = filename
    # sending image using errors-safe method
    await send_media_safe(message.answer_photo, 2, image_bytes, logger=logger)
    
    
# example of how to work with documents
@dp.message_handler(state=[UserStates.start, None], content_types=['document'])
@dp.throttled(anti_flood, rate=2)
async def reply_document(message: types.Message, state: FSMContext): 
    if message.document is not None:
        file_url = await message.document.get_url()
        document_data = await message.document.get_file()
        filename = os.path.basename(document_data['file_path'])
    else:
        await message.answer(
            "Can't recognize your attached document"
        )
        return
    
    document_bytes = await download_to_bytes(file_url)
    document_bytes.name = filename
    # sending document using errors-safe method
    await send_media_safe(message.answer_document, 2, document_bytes, thumb=filename, logger=logger)
        

### Keyboard example
@dp.message_handler(state=[UserStates.start, None], commands=['get_keyboard'])
@dp.throttled(anti_flood, rate=2)
async def get_keyboard_message(message: types.Message, state: FSMContext):
    await UserStates.choosing.set()
    await message.answer(
        "Example keyboard message",
        reply_markup=KEYBOARDS['example']['markup']
    )

# Keyboard answer handler
@dp.message_handler(IsNotCommand(), state=UserStates.choosing, content_types=['text'])
@dp.throttled(anti_flood, rate=2)
async def keyboard_handler_message(message: types.Message, state: FSMContext):
    result = message.text.strip()
    if result not in KEYBOARDS['example']['variants']:
        await message.answer('Choose variant from keyboard!')
        return
        
    await message.answer(
        "Ok!",
        reply_markup=KEYBOARDS['hide']
    )
    await UserStates.start.set()

    
async def on_startup(dispatcher):
    print('on_startup')
    
async def on_shutdown(dispatcher):
    print('on_shutdown')
    

if __name__ == "__main__":
    logger = setup_logger('test_bot.log')

    # auth
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)