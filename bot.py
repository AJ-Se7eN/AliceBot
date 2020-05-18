from telebot import TeleBot, types

from config import ADMIN_ID, TOKEN

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row("/Инфо","/StandUp",)
    bot.send_message(message.chat.id, f"Здравствуйте {message.from_user.first_name}!\
    \nЖелаете пройти стендапп опрос?", reply_markup=markup)


@bot.message_handler(commands=['Инфо'])
def send_about(message: types.Message):
    """Информация о боте"""
    bot.send_message(message, "Мы поможем вам заполнить информацию об участнике")


@bot.message_handler(commands=["StandUp"])
def register_group(message: types.Message):
    """Регистрация группы"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row('Alice','Game Guess Number', 'To do list', 'Parser')
    msg = bot.send_message(message.chat.id, 'Ваша группа?', reply_markup=markup)
    bot.register_next_step_handler(msg, register_work)

def register_work(message: types.Message):
    """Регистрация  работы"""
    global user_group
    user_group = message.text
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, 'Что вы сделали?', reply_markup=markup)
    bot.register_next_step_handler(msg, register_todo)


def register_todo(message: types.Message):
    """Регистрация плана"""
    global user_work
    user_work = message.text
    msg = bot.send_message(message.chat.id, 'Что вы будете делать?')
    bot.register_next_step_handler(msg, register_difficilties)


def register_difficilties(message: types.Message):
    """Регистрация имеющейся сложности"""
    global user_todo
    user_todo = message.text
    msg = bot.send_message(message.chat.id, 'Есть сложности?')
    bot.register_next_step_handler(msg, register_init)


def register_init(message: types.Message):
    """Инициализация и отправка данных пользователю так же админу"""
    global user_difficilties
    user_difficilties = message.text
    user_answer = f"{message.from_user.last_name} \n Ваша группа?: {user_group} \
        \nЧто вы сделали?: {user_work} \nЧто вы будете делать?: {user_todo} \nЕсть сложности?: {user_difficilties}"
    bot.send_message(message.chat.id, user_answer , parse_mode="Markdown")
    bot.send_message(ADMIN_ID, user_answer )

if __name__ == "__main__":
    bot.polling(none_stop=True)
