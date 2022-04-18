from aiogram.types import KeyboardButton
from requests import Response
from bs4 import BeautifulSoup
import requests
import json

def get_exhibit_keyboard(num_of_exhibits: int) -> list:
        """Returns a binary array with instances of KeyboardButton

        Args:
            num_of_exhibits (): _description_

        Returns:
            list: _description_
        """
        
        keyboard = [[], []]
        #generating keyboard
        
        
        for i in range(1, num_of_exhibits + 1):
                if i <= num_of_exhibits // 2:
                        keyboard[0].append(KeyboardButton(i))
                else:
                        keyboard[1].append(KeyboardButton(i))
        
        
        return keyboard

def check_photo_type(value, types: list):
        from bot.data_modules.exhibit_photo import ExhibitPhoto
        val_type = type(value)
        if not val_type in types:
            get_type = lambda elem: str(elem).split(" ")[1][1:-2]
            raise AttributeError(f"Value is supposed to be one of next types: {', '.join(list(map(get_type, ExhibitPhoto.ALLOWED_TYPES_OF_VALUES)))}")
    
    
def get_dioram_list(language_code, num_of_exhibits):
        from bot.data_modules.exhibit_photo import ExhibitPhoto
        dioram_list = ""

        for i in range(num_of_exhibits):
                current_exhibit_photo = ExhibitPhoto(i + 1) 
                
                dioram_list += f"{i+1}. {current_exhibit_photo.name[language_code]}\n"
                
        return dioram_list


def get_telegram_photo_url(file_id: str, bot_token: str):
        telegram_file_path = json.loads(requests.get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}").text)['result']["file_path"]
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{telegram_file_path}"
        return file_url
        
def find_telegram_photo_in_yandex(file_id: str, bot_token: str) -> Response:
        url = f"https://yandex.ru/images/search?rpt=imageview&url={get_telegram_photo_url(file_id=file_id, bot_token=bot_token)}"
        
        return requests.get(url)
        
def get_dioram_photo_index(html_to_parse: str, dioram_names: list, elem_to_search_in: str, classes: str = "") -> int:
        """Returns index of which name from dioram_names is in html_to_parse. If no name found in html, returns -1 

        Args:
            html_to_parse (str): html text that can be parsed using BeautifulSoup library
            dioram_names (list): a list with names to check in html_to_parse 

        Returns:
            int: _description_
        """
        
        soup = BeautifulSoup(html_to_parse, 'lxml')
        
        quotes = soup.find_all('div', class_="CbirObjectResponse-Title") or soup.find_all(elem_to_search_in, class_=classes)
        
        for quote in quotes:
                for i in range(len(dioram_names)):
                        if dioram_names[i] in quote:
                                return i
        
        return -1

def check_keyword_in_tag(keywords: list, tag: str):
        print(keywords)
        
        for keyword in keywords:
                if keyword in tag:
                        return True

        return False


def get_num_of_dioram(html: str, keywords: dict) -> int:
        soup = BeautifulSoup(html, 'lxml')
        
        quotes = soup.find_all('div', class_="CbirObjectResponse-Title") or soup.find_all('span', class_="Button2-Text")
        
        for quote in quotes:
                for key in keywords.keys():
                        print(quote, keywords[str(key)])
                        
                        if check_keyword_in_tag(keywords[key], str(quote)):
                                return int(key)


KEYWORDS = {
    "1": ["битва за москву", "битва под москвой", "Москва", "москва", "москвой"  "Москвой", "Битва за Москву", "Битва под Москвой"],
    "2": ["Сталинград", "сталинград", "Сталинградская битва", "сталинградская битва"], 
    "3": ["Ленинград", "Ленинграда", "ленинград", "ленинграда", "Блокада Ленинграда", "блокада ленинграда"],
    "4": ["Курская битва", "Курск", "Курская", "курск", "курская"],
    "5": ["Днепра", "Форсирование", "днепр", "форсирование",  "Форсирование Днепра"],
    "6": ["Берлин", "Берлина", "берлин", "берлина", "штурм берлина", "Штурм Берлина"]
}
