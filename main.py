from datetime import datetime
import datetimerange
from telebot import types, TeleBot
import json
from google_sheets import GoogleSheet

settings = json.loads(open(file="secrets.json", mode="r", encoding="UTF-8").read())
bot = TeleBot(token=settings["telegram_token"])
sheet = GoogleSheet(
    google_sheet_link=settings["google_sheet_link"],
    google_auth_file_path=settings["google_auth_file_path"],
)


@bot.message_handler(commands=["start"])
def start_handler(message):
    sticker_id = "CAACAgQAAxkBAAEF-fRjOJQ9_PVrCFv2NZPdVXkOS6pAIQACFgoAArHxyVOb0JkKNVNU_yoE"  # TODO:  сюда вставить ID стикера
    greeting = f'Привет, {message.from_user.first_name}. Меня зовут Полик и я {"red_heart"} играть в монополию. Поздравляю тебя с успешной регистрацией и желаю хорошей карьерной недели! Чтобы увидеть, что я умею - нажми на кнопку "Меню".'
    bot.send_sticker(message.chat.id, sticker_id)
    bot.send_message(message.chat.id, greeting, parse_mode="html")


@bot.message_handler(commands=["prize"])
def prize_handler(message):
    participant_id = message.from_user.id
    prize_message = f"Твой ID: <b>{participant_id}</b>. Скажи его организаторам в воскресенье и забирай свои призы!"
    bot.send_message(message.chat.id, prize_message, parse_mode="html")


@bot.message_handler(commands=["question"])
def question_handler(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_rules = types.InlineKeyboardButton(text="Правила", callback_data="rules")
    item_faq = types.InlineKeyboardButton(text="FAQ", callback_data="faq")
    markup_inline.add(item_rules, item_faq)
    bot.send_message(message.chat.id, "Что Вас интересует?", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: call.data == "rules")
def rules_handler(call):
    rules = f"<b>Правила монополии просты:</b>\n\n<u><i>1. Регистрация</i></u>\nДополнительно регистрироваться в монополии не нужно. Вы автоматически зарегистрированы, если используете бота.\n\n<u><i>2. Как заработать бренды и собрать монополию?</i></u>\nПолик может получать баллы за:\n     а)посещение мероприятий;\n     б)победу в мероприятии;\n     в)активное участие (например, вопросы спикеру).\nЧтобы собрать монополию, Полику нужно получить все бренды одного цвета. А если он соберет одну или несколько монополий, то в конце карьерной недели сможет получить один из 50 призов!\n\n<u><i>3. Полик не смог прийти на мероприятие от Ozon, значит ли это, что он больше не сможет получить себе этот бренд?</i></u>\nНет. Полик может получить <u>каждый</u> бренд минимум 2 раза. За активное участие и (или) победу в мероприятии он сможет самостоятельно выбрать любой бренд себе в коллекцию!\n\n<u><i>4. Как Полику узнать, какие бренды он уже собрал?</i></u>\nЧтобы посмотреть свои бренды и монополии, достаточно написать в чат /brands.\n\n<u><i>5. Как Полику получить приз?</i></u>\nПриходи на мероприятия в воскресенье, введи команду /prize, покажи организатору свой ID и забирай подарки!\n\n<u><i>6. Полик не может найти ответ на свой вопрос. Что делать?</i></u>\nЧтобы связаться с организаторами - напиши в чат /help."
    bot.send_message(call.message.chat.id, rules, parse_mode="html")


@bot.callback_query_handler(func=lambda call: call.data == "faq")
def faq_handler(call):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_register = types.KeyboardButton("Регистрация")
    item_brands = types.KeyboardButton("Как собрать бренды?")
    item_prize = types.KeyboardButton("Как получить приз?")
    item_no_answer = types.KeyboardButton("Нет ответа на мой вопрос")
    markup_reply.add(item_register, item_brands, item_prize, item_no_answer)
    bot.send_message(call.message.chat.id, "Частые вопросы", reply_markup=markup_reply)


@bot.message_handler(
    func=lambda message: message.text in ["вшм", "аналитик", "маркетинг"]
)
def activities_handler(message):
    actions = {  # format [date_start, date_end]
        "вшм": [
            datetime(year=2022, month=10, day=10, hour=21, minute=0, second=0),
            datetime(year=2022, month=10, day=10, hour=23, minute=0, second=0),
        ],
        "аналитик": [
            datetime(year=2022, month=10, day=10, hour=21, minute=0, second=0),
            datetime(year=2022, month=10, day=10, hour=23, minute=0, second=0),
        ],
        "маркетинг": [
            datetime(year=2022, month=10, day=10, hour=21, minute=0, second=0),
            datetime(year=2022, month=10, day=10, hour=23, minute=0, second=0),
        ],
    }
    now_time = datetime.now()
    action = actions[message.text.lower()]
    is_in_time = now_time in datetimerange.DateTimeRange(action[0], action[1])
    if is_in_time:
        if "вшм" in message.text.lower():
            bot.send_message(message.chat.id, f"это правильный ответ vmsh")
        elif "аналитик" in message.text.lower():
            bot.send_message(message.chat.id, f"это правильный ответ analytic")
        elif "маркетинг" in message.text.lower():
            bot.send_message(message.chat.id, f"это правильный ответ marketing")
    else:
        bot.send_message(message.chat.id, "Время события еще не пришло!")


@bot.message_handler(content_types=["text"])
def faq_and_err_handler(message):
    faq_responses = {
        "Регистрация": f"Вы уже зарегистрированы.",
        "Как собрать бренды?": f"тут будет текст",
        "Как получить приз?": f'Ваш ID: {message.from_user.id}. Назовите его организаторам в воскресенье и получите приз {"money_bag"}',
        "Нет ответа на мой вопрос": "f'Если Вы не нашли ответ на свой вопрос, сделайте следующее: прочитайте заново правила, FAQ, напишите @andre1kazakoff'",
    }

    if message.text in faq_responses.keys():
        bot.send_message(message.chat.id, faq_responses[message.text])

    else:
        bot.send_message(
            message.chat.id,
            f"к сожалению, это неправильный ответ. либо мой функционал не предусматривает это",
        )


bot.polling(none_stop=True)
