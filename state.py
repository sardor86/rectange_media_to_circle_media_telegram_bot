from aiogram.dispatcher.filters.state import StatesGroup, State


class UploadVidioPhotoFile(StatesGroup):
    vidio = State()
    photo = State()
