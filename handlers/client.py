from aiogram import types,Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import bot
from keyboards import kb_client,kb_clientProcess
from keys_token import tokens
from data_base import sql_db

class GroupInfo():
    def chatId():
        id = ''
        return id


class FSMSendOrder(StatesGroup):
    chatID = State()
    photo = State()
    description = State()
    check = State()
    sucsPay = State()


#@dp.message_handler(commands=['start','help'])
async def command_start(message:types.Message):
    await bot.send_sticker(message.from_user.id,sticker='CAACAgIAAxkBAAIEzmOoZ3LIror1zlmRgRitlcvKKYgFAAI2FgACcmugS6XaTV2HP2QpLAQ')
    await bot.send_message(message.from_user.id, 'Надішліть фото, яке ви хочете відфотошопити (файлом, тобто без стиснення)',reply_markup=kb_clientProcess)
    await FSMSendOrder.photo.set()

async def getIDMaker(message:types.Message):
    print(message.from_user.id)

#@dp.message_handler(state="*", commands=['Cancel'])
#@dp.message_handler(Text(equals='Cancel',ignore_case=True),state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')
    await bot.send_message(message.from_user.id, "Напишіть у чат '/start' або натисність на кнопку '/start'" ,reply_markup=kb_client)

#@dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    try:
        if "image" == message.document.mime_type[:5]:
            async with state.proxy() as data:
                data['chatID'] = message.chat.id
                data['photo'] = message.document.file_id
            await FSMSendOrder.next()
            await message.reply('Введіть коментарій (що ви хочете, які деталі соблюдати і тд) (коментарій повинен бути невелики, не більше 1024 символів)')
        else:
            await message.reply('Це був не файл фотографії :)')
    except:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Щось пішло не так, зверніться в службу підтримки')

#@dp.message_handler(state=FSMAdmin.price)
async def load_price(chatID, comments, photo):
     # try:
     #    async with state.proxy() as data:
     #        data['price'] = float(message.text)
     #    #await sql_db.sql_add_command(state)
     #    await sendGet(state)
     #    await state.finish()
     # except ValueError:
     #     await message.reply('Введіть тільки цифру, без додаткових символів, типу - грн')
     # pricePhoto = [types.LabeledPrice(label="Make a funny photo",amount = 500)]
     await bot.send_message(chatID,
                            "Використайте цей номер картки для оплати: `4242 4242 4242 4242`"
                            "\n\nThis is your demo invoice:", parse_mode='Markdown')
     await bot.send_invoice(chatID, title='Make a funny photo',
                            description=comments,
                            provider_token=tokens.paytoken(),
                            currency='usd',
                            photo_url='https://www.wikihow.com/images_en/thumb/e/e7/Caricature-Step-7-preview.jpg/670px-Caricature-Step-7-preview.jpg',
                            photo_height=512,  # !=0/None or picture won't be shown
                            photo_width=512,
                            #photo_size=512,
                            is_flexible=False,  # True If you need to set up Shipping Fee
                            prices=[types.LabeledPrice(label="Make a funny photo",amount = 500)],
                            start_parameter='EasyOfferPhoto',
                            payload=str(photo))


#@dp.message_handler(state = FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    try:
        if(len(message.text) < 1024):
            async with state.proxy() as data:
                data['description'] = message.text
                await load_price(data['chatID'],data['description'], data['photo'])
            await FSMSendOrder.next()
        else: await message.reply('Зробіть опис коротше')
    except:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Щось пішло не так, зверніться в службу підтримки')



async def sendGet(stateData):
    async with stateData.proxy() as data:
        postWork = types.InlineKeyboardMarkup()
        postWork.add(types.InlineKeyboardButton(
            text="Take work",
            callback_data="newWork "+str(data['chatID']))
        )
        await bot.send_document(
            chat_id=GroupInfo.chatId(),
            document=data['photo'],
            caption=data['description'],
            reply_markup=postWork
        )


# async def shipping(shipping_query: types.ShippingQuery):
#     shipping_options = [
#     types.ShippingOption(id='instant', title='Delivery').add(types.LabeledPrice('Delivery', 300)),
#     types.ShippingOption(id='pickup', title='Local pickup').add(types.LabeledPrice('Pickup', 0)),]
#     await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
#                                     error_message='Oh, seems like our Dog couriers are having a lunch right now.'
#                                                   ' Try again later!')


async def checkout(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")
    await FSMSendOrder.next()


async def got_payment(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.chat.id,
                               'Hoooooray! Thanks for payment! We will proceed your order for `{} {}`'
                               ' as fast as possible! Stay in touch.'.format(
                                   message.successful_payment.total_amount / 100, message.successful_payment.currency),
                               parse_mode='Markdown',reply_markup=kb_clientProcess)
        await sendGet(state)
        await state.finish()
    except:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Щось пішло не так, зверніться в службу підтримки')



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start','help'])
    dp.register_message_handler(getIDMaker, commands=['invite'])
    dp.register_message_handler(cancel_handler, Text(equals='Cancel',ignore_case=True), state=FSMSendOrder)
    dp.register_message_handler(cancel_handler,state=FSMSendOrder,commands=['Cancel'])
    dp.register_message_handler(load_photo,content_types=['document'],state=FSMSendOrder.photo)
    dp.register_message_handler(load_description,state=FSMSendOrder.description)
    # dp.register_shipping_query_handler(shipping, lambda query: True)
    dp.register_pre_checkout_query_handler(checkout, lambda query: True,state=FSMSendOrder.check)
    dp.register_message_handler(got_payment, content_types=types.message.ContentTypes.SUCCESSFUL_PAYMENT,state=FSMSendOrder.sucsPay)
