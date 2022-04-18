#MONGO DATABASE CONFIGS
MONGO_DB_NAME = "victory-museum-database"
MONGO_DB_PHOTO_COLLECTION_NAME = "photo-collection"
MONGO_DB_URI_FOR_CLIENT = "mongodb://localhost:27017/"
#Number of exhibits
NUMBER_OF_EXHIBITS = 6 
#Default language that will be chosen if no user language in DB
DEFAULT_LANGUAGE_CODE = "ru"
#keywords
KEYWORDS = {
    "1": ["Москва", "Москвой", "Битва за Москву", "Битва под Москвой", "битва за москву", "битва под москвой"],
    "2": ["Сталинград", "сталинград", "Сталинградская битва", "сталинградская битва"], 
    "3": ["Ленинград", "Ленинграда", "ленинград", "ленинграда", "Блокада Ленинграда", "блокада ленинграда"],
    "4": ["Курская битва", "Курск", "Курская", "курск", "курская"],
    "5": ["Днепра", "Форсирование", "днепр", "форсирование",  "Форсирование Днепра"],
    "6": ["Берлин", "Берлина", "берлин", "берлина", "штурм берлина", "Штурм Берлина"]
}