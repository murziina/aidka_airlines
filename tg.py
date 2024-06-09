from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types.web_app_info import WebAppInfo

bot = Bot(token='7488175920:AAFQrz1IPsKVWoMN9USy6kN0pImdatduvYU')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://example.com')))
    await message.answer('привет, мой друг', reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp)