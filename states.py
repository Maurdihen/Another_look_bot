from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    ChooseCat = State()
    Enroll = State()
    Subgroup = State()
    ChooseDay = State()
    ChooseTime = State()
    GetNumber = State()
    ReqestCont = State()
    PhoneNumber = State()