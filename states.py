from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    GetNumber = State()
