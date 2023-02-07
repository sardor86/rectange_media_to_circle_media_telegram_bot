from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import mkdir
from os.path import exists
from time import time

from config import TOKEN, path
from state import UploadVidioPhotoFile
from video_redactor import video_redactor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['cansel'], state='*')
async def start_or_help_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Отменена')


@dp.message_handler(commands=['start', 'help'])
async def start_or_help_command(message: types.Message):
    await message.reply('Чтобы начать напишите /begin')


@dp.message_handler(commands=['begin'])
async def start_or_help_command(message: types.Message):
    await message.reply('Отправте нам видио мы из квадрата сделаем круг и на фон поместим фото')
    await bot.send_message(message.from_user.id, 'В любой момент вы можете написать /cansel для отмены')
    await UploadVidioPhotoFile.vidio.set()


@dp.message_handler(content_types=types.ContentType.VIDEO, state=UploadVidioPhotoFile.vidio)
async def start_get_video(message: types.Message, state: FSMContext):
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    async with state.proxy() as data:
        data['video'] = file

    await message.reply('Отправте нам фотографию')
    await UploadVidioPhotoFile.photo.set()


@dp.message_handler(lambda message: not message.video, state=UploadVidioPhotoFile.vidio)
async def get_vidio(message: types.Message):
    await message.reply('Это не видио')


@dp.message_handler(content_types=types.ContentType.PHOTO, state=UploadVidioPhotoFile.photo)
async def start_get_video(message: types.Message, state: FSMContext):
    file_name = path + f'/files/{"".join(str(time()).split("."))}'

    file_info = await bot.get_file(message.photo[-1].file_id)
    await message.photo[-1].download(f'{file_name}.{file_info.file_path.split(".")[-1]}')

    file_photo = f'{file_name}.{file_info.file_path.split(".")[-1]}'
    file_result = f'{file_name}result.mp4'

    async with state.proxy() as data:
        await bot.download_file(data['video'].file_path, file_name + '.' + data['video'].file_path.split('.')[-1])
        file_video = f'{file_name}.{data["video"].file_path.split(".")[-1]}'

    await state.finish()

    await video_redactor(file_photo, file_video, file_result)
    await bot.send_video(message.chat.id, file_result)


@dp.message_handler(lambda message: not message.photo, state=UploadVidioPhotoFile.photo)
async def get_vidio(message: types.Message):
    await message.reply('Это не фото')


if __name__ == '__main__':
    if not exists(path + '/files'):
        mkdir(path + '/files')

    executor.start_polling(dp)
