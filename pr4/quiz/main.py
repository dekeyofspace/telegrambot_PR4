import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '2037710159:AAGxUqF7bw_kHzXYG1QODsHN7zZ5d-8TS7Q'

bot = Bot(token = API_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

class From(StatesGroup):
	firstname = State()
	lastname = State()
	group = State()
	startedu = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
	await From.firstname.set()
	await message.reply("Привет! Как тебя зовут?")

@dp.message_handler(state=From.firstname)
async def process_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['firstname'] = message.text
	await From.next()
	await message.reply("Какая у тебя фамилия?")

@dp.message_handler(state=From.lastname)
async def process_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['lastname'] = message.text
	await From.next()
	await message.reply("В какой группе ты учишься?")

@dp.message_handler(lambda message: message.text, state=From.group)
async def process_group(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['group'] = message.text
	await From.next()

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("2018","2019","2020","2021")

	await message.reply("В какой году ты поступил?", reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["2018","2019","2020","2021"], state=From.startedu)
async def process_year_invalid(message: types.Message):
	return await message.reply("Ответ не верный. Выберите год из предложенного.")

@dp.message_handler(state=From.startedu)
async def process_year(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['startedu'] = message.text

	markup = types.ReplyKeyboardRemove()

	await bot.send_message(
		message.chat.id,
		md.text(
			md.text('Рад познакомится, ', md.bold(data['firstname'] + ' ' + data['lastname'])),
			md.text('Твоя группа: ', data['group']),
			md.text('Начал обучаться в ', data['startedu']),
			sep='\n'),
		reply_markup=markup,
		parse_mode=ParseMode.MARKDOWN,
		)

	await state.finish()



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)