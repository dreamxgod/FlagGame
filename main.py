from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from os import environ
from glob import glob
from random import randrange
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
API_TOKEN = environ.get('TELEGRAM_BOT_TOKEN')
if API_TOKEN == None:
    logging.fatal(
        "Set your's bot token in $TELEGRAM_BOT_TOKEN environment variable.\n \
        To do it, run the following command: \n \
        export TELEGRAM_BOT_TOKEN='<your_token'>")
    exit(-1)

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Game(StatesGroup):
    question = State()
    answer = State()


files = glob("./pictures/*.png")


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Game.question.set()
    await message.reply("Lets play the game (type something to continue)")


@dp.message_handler(state=Game.question)
async def question_handler(message: types.Message, state: FSMContext):
    number = randrange(0, len(files))
    file = files[number]
    answer = Path(file).stem
    async with state.proxy() as data:
        data['answer'] = answer

    logging.info(file)
    await Game.next()
    await bot.send_photo(chat_id=message.chat.id, photo=open(file, 'rb'))
    await message.reply("Guess country by flag")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Game.answer)
async def process_answer(message: types.Message, state: FSMContext):
    # Update state and data
    answer = message.text
    async with state.proxy() as data:
        if answer.casefold() == str(data['answer']).casefold():
            await Game.question.set()
            reply = "correct! (type something to continue)"
        else:
            reply = "try again (or reply /cancel to surrender)"

    # Configure ReplyKeyboardMarkup

    await message.reply(reply)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)