from aiogram import types,Dispatcher
from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import  ReplyKeyboardRemove
from data_base import sql_db

class DownloadPhoto(StatesGroup):
    makerID = State()
    userID = State()
    photo = State()


class GroupInfo():
    def chatId():
        id = ''
        return id

async def takeWork(callback_query:types.CallbackQuery):
    try:
        idMaker = str(callback_query.from_user.id)
        readiness = await sql_db.sql_add_readReadiness(idMaker)
        if readiness != 1:
            userID = callback_query.data.replace('newWork ','')
            await bot.send_document(chat_id=idMaker, document=callback_query.message.document.file_id)
            await bot.send_message(chat_id=idMaker, text=callback_query.message.caption)
            await bot.send_message(chat_id=idMaker, text='Очікування на фото (БЕЗ СТИСНЕННЯ), щоб завантажити фото спочатку пропишіть команду "/download"')
            await callback_query.message.delete()
            workInfo = [userID, idMaker]
            sql_db.sql_add_newWork(workInfo)
        else: await bot.send_message(chat_id=idMaker, text='У тебе ще є незакінчена робота')
        await callback_query.answer()
    except: await bot.send_message(chat_id=callback_query.from_user.id, text='Щось пішло не так, зверніться в службу підтримки')


async def command_download(message:types.Message, state: FSMContext):
    try:
        if sql_db.sql_find_makerID(message.from_user.id):
            await message.reply("Привіт, завантажуй свою готову роботу!")
            async with state.proxy() as data:
                data['makerID'] = message.from_user.id
                data['userID'] = sql_db.sql_find_userID(data['makerID'])
            await DownloadPhoto.photo.set()
    except: await message.reply('Щось пішло не так, зверніться в службу підтримки')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')
    await bot.send_message(message.from_user.id, "Напишіть у чат '/download', якщо знову будете готові відправити фото", reply_markup=ReplyKeyboardRemove )


async def beSure(stateData):
    async with stateData.proxy() as data:
        work = types.InlineKeyboardMarkup()
        work.add(types.InlineKeyboardButton(
            text="Yes",
            callback_data="sure")
        ).add(types.InlineKeyboardButton(
            text="No",
            callback_data="notSure")
        )
        await bot.send_document(
            chat_id=data['makerID'],
            document=data['photo'],
            caption='Ви впевненні, що це фото готове?',
            reply_markup=work
        )


async def makerSure(callback_query:types.CallbackQuery, state: FSMContext):
    try:
        await sql_db.sql_add_finishedWork(state)
        await callback_query.message.delete()
        async with state.proxy() as data:
            await bot.send_document(chat_id=data['userID'], document=data['photo'])
        await state.finish()
        await callback_query.answer(text='Робота зроблена, молодець!', show_alert=True)
    except: await bot.send_message(chat_id=callback_query.from_user.id,text='Щось пішло не так, зверніться в службу підтримки')

async def makerNotSure(callback_query:types.CallbackQuery, state: FSMContext):
    try:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback_query.answer('Ок',show_alert=True)
        await bot.send_message(callback_query.from_user.id, "Напишіть у чат '/download', якщо знову будете готові відправити фото" )
    except:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Щось пішло не так, зверніться в службу підтримки')


async def load_photo(message: types.Message, state: FSMContext):
    if "image" == message.document.mime_type[:5]:
        async with state.proxy() as data:
            data['photo'] = message.document.file_id
        await beSure(state)
        # await sql_db.sql_add_finishedWork(state)
        # await state.finish()
    else:
        await message.reply('Це був не файл фотографії:)')




def register_handlers_makers(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, Text(equals='Cancel',ignore_case=True), state=DownloadPhoto)
    dp.register_message_handler(cancel_handler,state=DownloadPhoto,commands=['Cancel'])
    dp.register_callback_query_handler(takeWork, lambda x: x.data and x.data.startswith('newWork '))
    dp.register_message_handler(command_download, commands=['download'])
    dp.register_callback_query_handler(makerSure, lambda x: x.data and x.data.startswith('sure'), state=DownloadPhoto)
    dp.register_callback_query_handler(makerNotSure, lambda x: x.data and x.data.startswith('notSure'), state=DownloadPhoto)
    dp.register_message_handler(load_photo,content_types=['document'],state=DownloadPhoto.photo)
