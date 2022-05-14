from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from bot.configs.bot_token import TOKEN
from bot.configs.messages import start_messages, incorrect_exhibit_num_messages, greater_exhibit_num_messages, incorrect_photo_message
from bot.configs.config import  NUMBER_OF_EXHIBITS, KEYWORDS, DEFAULT_LANGUAGE_CODE
from bot.data_modules.exhibit_photo import ExhibitPhoto
from bot.utils.utils import get_exhibit_keyboard, get_dioram_list, find_telegram_photo_in_yandex, get_num_of_dioram
import bot.data_modules.data_maker
import logging



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
logger = logging.getLogger()

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)



@dispatcher.message_handler(commands=['start'])
async def handle_start(message: types.Message):
        bot =  Bot.get_current()
        user =  types.User.get_current()
        me = await bot.get_me()
        
        user_id = user.id
        user_name = user.full_name
        user_first_name = user.first_name
        bot_name = me.first_name
        language_code = user.language_code
        
        logger.info(f"{user_name} sent start command")
        
        keyboard = ReplyKeyboardMarkup(get_exhibit_keyboard(NUMBER_OF_EXHIBITS), resize_keyboard=True)
        
        message_to_send = start_messages.get(language_code) or start_messages["en"]
        
        try:
                dioram_list = get_dioram_list(language_code, NUMBER_OF_EXHIBITS)
        except KeyError:
                dioram_list = get_dioram_list("ru", NUMBER_OF_EXHIBITS)
        
        await message.reply(message_to_send.format(first_name=user_first_name, bot_name=bot_name, dioram_list=dioram_list), parse_mode="html", reply_markup=keyboard)



@dispatcher.message_handler(content_types=["text"])
async def handle_text(message: types.Message):
        user = types.User.get_current()
        user_name = user.full_name
        
        language_code = user.language_code
        
        try:
                exhibit_num = int(message.text)
                if exhibit_num <= NUMBER_OF_EXHIBITS:
                        photo = ExhibitPhoto(exhibit_num)
                        
                        photo_name = photo.name.get(language_code) or photo.name[DEFAULT_LANGUAGE_CODE]
                        
                        await message.reply_photo(photo=photo.telegram_file_id, caption=photo_name, parse_mode="html")
                        logger.info(f"User chose diaram with next number: {exhibit_num}. So he got photo with next name: {photo.name}. User's language: {language_code}")
                else:
                        message_to_send = greater_exhibit_num_messages.get(language_code) or greater_exhibit_num_messages["en"]
                        await message.reply(message_to_send.format(number_of_exhibits=NUMBER_OF_EXHIBITS), parse_mode="html")
                        logger.info(f"{user_name} entered number of dioram, which is greater than total number of dioram. Input: {message.text}. User's language: {language_code}")
                        
        except ValueError:
                message_to_send = incorrect_exhibit_num_messages.get(language_code) or incorrect_exhibit_num_messages["en"]
                await message.reply(message_to_send.format(number_of_exhibits=NUMBER_OF_EXHIBITS), parse_mode="html")
                logger.info(f"{user_name} entered incorrect number of dioram. Input: {message.text}. User's language: {language_code}")


@dispatcher.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
        user = types.User.get_current()
        
        user_id = user.id
        user_name = user.full_name
        me = await bot.get_me()
        language_code = user.language_code
        
        photo = message.photo
        
        response = find_telegram_photo_in_yandex(photo[2]["file_id"], TOKEN)
        
        
        num = get_num_of_dioram(response.text, KEYWORDS)
        
        if num:        
                photo = ExhibitPhoto(num)

                photo_name = photo.name.get(language_code) or photo.name[DEFAULT_LANGUAGE_CODE]        
                photo_description = photo.description.get(language_code) or photo.description[DEFAULT_LANGUAGE_CODE]
                
                message_to_send = f"{photo_name}\n\n{photo_description}"
                
                await message.reply_photo(photo.telegram_file_id, caption=message_to_send, parse_mode="html")
        else:
                await message.reply(incorrect_photo_message.get(language_code) or incorrect_photo_message['en'], parse_mode="html")
        
        logger.info(f"{user_name} sent a photo. User's language: {language_code}")
