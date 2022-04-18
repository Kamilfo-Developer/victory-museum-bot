from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from bs4 import BeautifulSoup
from bot.configs.bot_token import TOKEN
from bot.configs.messages import start_messages, incorrect_exhibit_num_messages, greater_exhibit_num_messages, incorrect_photo_message
from bot.configs.config import  NUMBER_OF_EXHIBITS, KEYWORDS, DEFAULT_LANGUAGE_CODE
from bot.data_modules.exhibit_photo import ExhibitPhoto
from bot.utils.utils import get_exhibit_keyboard, get_dioram_list, find_telegram_photo_in_yandex, get_num_of_dioram
import logging
#region db_data_creator


"""
FIRST = "AgACAgIAAxkBAAIJ4mJa8Y3iXPFEFb39RE-2SyrdGHcXAAKwvTEbzfjYSl7qR8EsWFPyAQADAgADcwADJAQ"
SECOND = "AgACAgIAAxkBAAIJ5mJa8h4wdCOvg_RGrDsRgQ0Mt4KZAAIivTEb5J7YSgx9CKF9IFfWAQADAgADcwADJAQ"
THIRD = "AgACAgIAAxkBAAIJ6GJa8kcqE1-KeKSCtczl5X5QpyUwAAIjvTEb5J7YStC8dBrceMBPAQADAgADcwADJAQ"
FOURTH = "AgACAgIAAxkBAAIJ6mJa8nJfG_jYoB7J_Alrgr_tViLPAAIlvTEb5J7YShfq7Qp-KxOvAQADAgADcwADJAQ"
FIFTH = "AgACAgIAAxkBAAIJ7GJa8o6tk0ejwfTObpye3FGR9oPvAAInvTEb5J7YSlzo8gPvwhZNAQADAgADcwADJAQ"
SIXTH = "AgACAgIAAxkBAAIJ7mJa8rlU5pStSySUYqnG8DrVIFsqAAIovTEb5J7YSo_G08yAlOj7AQADAgADcwADJAQ"


photo1 = ExhibitPhoto(1)

photo1.name = {
        "ru": "Контрнаступление советских войск под Москвой в декабре 1941 года"
}

photo1.file_name = "1.jpg"

photo1.description = {
        "ru":" В основу сюжета положены события, происходившие в ноябре-декабре 1941 г. в районе г. Яхромы Дмитровского района Московской области. В центре полотна – идущие к переправе через канал Москва-Волга бойцы сибирских и уральских частей, прибывшие для пополнения 1-й Ударной армии Западного фронта. В результате зимнего контрнаступления Красной Армии замысел гитлеровского командования по овладению Москвой с северо-западного направления был сорван, враг был отброшен от Москвы на 100-250 км. Прямая угроза захвата столицы была ликвидирована."
}

photo1.telegram_file_id = FIRST


photo2 = ExhibitPhoto(2)

photo2.name = {"ru": "Сталинградская битва. Соединение фронтов"}

photo2.description = {
        "ru": "В основу сюжета положено историческое событие – соединение войск Юго-Западного и Сталинградского фронтов 23 ноября 1942 г. в районе г. Калач и поселка Советский. Художники показали кульминационный момент встречи танкистов 45-й и 69-й танковых бригад 4-го танкового корпуса (командир генерал-майор А.Г.Кравченко) с бойцами 36-й механизированной бригады 4-го механизированного корпуса (командир генерал-майор В.Т.Вольский). Сталинградская битва, в которой участвовали с обеих сторон более 2 млн. человек, происходила на территории в 100 тыс. кв. км. И продолжалась 200 дней и ночей. Сталинградская битва положила начало коренному перелому в Великой Отечественной войне 1941-1945 гг. в пользу СССР и его союзников."
} 

photo2.file_name = "2.jpg"

photo2.telegram_file_id = SECOND


photo3 = ExhibitPhoto(3)

photo3.name = {"ru": "Блокада Ленинграда"}

photo3.description = {
        "ru": "Эта диорама принципиально отличается от других: здесь нет боев, солдат, танков, порохового дыма. Зритель видит панораму Невы, стрелку Васильевского острова, Петропавловскую крепость, справа – канал Грибоедова, Банковский мостик. Этот вид не соответствует реальной топографии, он умышленно скадрирован, чтобы создать образ Великого города, который воспринимается как символ стойкости и героизма защищавших его людей, выдержавших 900 дней изнурительной блокады. На боковых стенах диорамного зала изображены ленинградцы, героически защищавшие свой город. Среди них – поэтесса Ольга Берггольц, композитор Дмитрий Шостакович, писатель Александр Крон. В смертельной схватке с жестоким врагом, преодолев тягчайшие трудности блокады, ленинградцы выстояли и победили."
}

photo3.file_name = "3.jpg"

photo3.telegram_file_id = THIRD


photo4 = ExhibitPhoto(4)

photo4.name = {"ru": "Курская битва"}

photo4.description = {
        "ru": "В основу сюжета положены исторические события лета 1943 г., завершившие коренной перелом в ходе Великой Отечественной войны, - разгром немецко-фашистских войск на Курской дуге. Посвящая свою работу стратегической операции на Курской дуге, автор берет лишь один ее день – 12 июля 1943 г., когда в районе Прохоровки сошлись в лобовом сражении две танковые армады. С обеих сторон насчитывалось до 1200 танков самоходно-артиллерийских установок. Это было одним из самых крупных встречных танковых сражений Второй мировой войны. По словам самого художника, он стремился воспроизвести «гигантский огненный котел на красно-рыжей, как раскаленный металл, земле». Сражение под Прохоровкой выиграли советские войска. Враг был измотан и обескровлен, по всему Курскому выступу началось его отступление. 5 августа в честь освобождения Орла и Белгорода в Москве был произведен первый салют. Курская битва завершилась 23 августа 1943 г. взятием Харькова."
}

photo4.file_name = "4.jpg"

photo4.telegram_file_id = FOURTH


photo5 = ExhibitPhoto(5)

photo5.name = {"ru": "Форсироване Днепра"}

photo5.description = {
        "ru": "В основу сюжета положено форсирование реки Днепр в сентябре-октябре 1943 г. на киевском направлении. Выйдя к Днепру, советские войска с ходу приступили к форсированию могучей реки. Используя любые подручные средства, преодолевая ожесточенное сопротивление врага, части Красной Армии переправлялись через Днепр и захватывали плацдармы на его правом берегу. Широкой гладью величественного Днепра диорама как бы поделена на две части. В левой, освещенной ярким солнечным светом, изображены заднепровские дали. Оттуда, с востока, идет свет надежды освобождения. Но чем ближе к западу, тем темнее становятся тона. Картины жизни и смерти перемешались: идет бой не на жизнь, а на смерть за каждую пядь земли. Автор диорамы – участник Великой Отечественной войны – считает эту переправу обобщенным образом всех днепровских переправ. Он отдает дань памяти и уважения всем тем, кто сражался, был ранен или пал в сражении при форсировании великой и могучей реки."
}

photo5.file_name = "5.jpg"

photo5.telegram_file_id = FIFTH


photo6 = ExhibitPhoto(6)

photo6.name = {"ru": "Штурм Берлина"}

photo6.description = {
        "ru": "Главным композиционным центром диорамы выбрана северо-восточная часть парка Тиргартен с рейхстагом. Сюда 29 арпеля 1945 г., сломив сопротивление немецко-фашистских войск, вышли передовые части 79-го стрелкового корпуса 3-й Ударной армии – 150-я стрелковая дивизия генерал-майора В.М.Шатилова и 171-я стрелковая дивизия полковника А.И.Негоды. Художник воспроизводит не только завершающий этап войны, но и отдельные героические подвиги советских войнов. В траншее мы видим полковника Ф.М.Зинченко с сержантом М.А.Егоровым и младшим сержантом М.В.Кантария, в руках одного из них – Знамя Победы, которое поздним вечером 30 апреля будет водружено на крыше рейхстага. 30 апреля 1945 г. части 3-й Ударной и 8-й Гвардейской армии штурмовали рейхстаг. 2 мая к 15 часам сопротивление противника полностью прекратилось, остатки берлинского гарнизона сдались в плен. 8 мая в пригороде Берлина Карлсхорсте был подписан акт о безоговорочной капитуляции Германии."
}

photo6.file_name = "6.jpg"

photo6.telegram_file_id = SIXTH
"""
#endregion

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
                        
                        await message.reply_photo(photo=photo.telegram_file_id, caption=photo_name)
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
                
                await message.reply_photo(photo.telegram_file_id, caption=message_to_send)
        else:
                await message.reply(incorrect_photo_message.get(language_code) or incorrect_photo_message['en'])
        
        logger.info(f"{user_name} sent a photo. User's language: {language_code}")
