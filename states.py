from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    start = State()
    choosing = State()
    processing = State()

not_processing_state = [None, UserStates.start, UserStates.choosing]