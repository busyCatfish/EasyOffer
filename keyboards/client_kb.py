from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Start')
b2 = KeyboardButton('/Cancel')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b1)

kb_clientProcess = ReplyKeyboardMarkup(resize_keyboard=True)
kb_clientProcess.row(b2)