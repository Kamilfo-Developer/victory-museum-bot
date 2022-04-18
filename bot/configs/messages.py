start_messages = {
    "ru": "Доброго времени суток, {first_name}!\n\nЯ - <b>{bot_name}</b>, бот <b><a href=\"https://victorymuseum.ru/\">\"Музея Победы\"</a></b>.\nМеня создали, чтобы помочь Вам узнать больше про диорамы нашего музея.\n\nВот список диорам:\n{dioram_list}\nЕсли Вы хотите получить фото диорамы с названием - отправьте мне её номер или выберете его на клавиатуре.\nА если Вы хотите узнать подробности про ту или иную диораму - просто отправьте мне её фото!\n",
    "en": "Hello there, {first_name}!\n\nI am <b>{bot_name}</b>, a bot of <b><a href=\"https://victorymuseum.ru/for-visitors/museum-for-china/en/\">\"Victory Museum\"</a></b>.\nI was created to help you in exploring diorams of our museum.\n\nIf you'd like to find out more about a dioram just send me its photo!\n",
}

greater_exhibit_num_messages = {
    "ru": "Похоже Вы ввели номер диорамы, который превышает число самих диорам!\n\nВсего диорам {number_of_exhibits}, так что Вы можете ввести число только от 1 до {number_of_exhibits}.",
    "en": "It looks like the number of the dioram you entered is greater than the number of all the diorams!\n\nIn total there are {number_of_exhibits} of them, so you can enter only a number in range from 1 to {number_of_exhibits}.",
}

incorrect_exhibit_num_messages = {
    "ru": "Похоже Вы ввели некорректный номер диорамы. Это число должно быть в диапазоне от 1 до {number_of_exhibits}.",
    "en": "It looks like you entered incorrect number of the dioram. The number must be in range from 1 to {number_of_exhibits}.",
}

incorrect_photo_message = {
    "ru": "Извините, но я не могу понять, какую именно диораму Вы имеете ввиду.\n\nПожалуйста, попробуйте сделать новое фото экспоната и прислать новое фото мне.",
    "en": "I am sorry, but I can't understand what kind of a dioram is represented on your picture.\n\nCould you make a new photo and send it to me?"
}