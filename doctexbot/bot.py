# install pyTelegramBotAPI

import telebot
from commands.cmd_list import cmds
from rest.process_ro import process_ro_full

token = '5891037858:AAHOBx7fHOtvD7eQO9IkszynRWuo38bQu6U'

# connection
bot = telebot.TeleBot(token)

last_messages = {}
forms = {}
# {
#     "chat_id": {
#         "doc": "ro",
#         "data": {
#             ...
#         }
#     }
# }


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, cmds.get('help'))


@bot.message_handler(commands=['loadro'])
def load_ro(message):
    bot.send_document(message.chat.id, open('docs/ro.tex', encoding='utf-8'))


@bot.message_handler(commands=['loadtz'])
def load_tz(message):
    bot.send_document(message.chat.id, open('docs/tz.tex', encoding='utf-8'))


@bot.message_handler(commands=['loadpmi'])
def load_pmi(message):
    bot.send_document(message.chat.id, open('docs/pmi.tex', encoding='utf-8'))


@bot.message_handler(commands=['loadtp'])
def load_tp(message):
    bot.send_document(message.chat.id, open('docs/tp.tex', encoding='utf-8'))


@bot.message_handler(commands=['loadpz'])
def load_pz(message):
    bot.send_message(message.chat.id, cmds.get('loadpz'))
    # bot.send_document(message.chat.id, open('docs/pz.tex', encoding='utf-8'))


@bot.message_handler(commands=['ro'])
def fill_ro(message):
    bot.send_message(message.chat.id, cmds.get('ro'))
    bot.send_message(message.chat.id, 'Какая должность у вашего наставника?')
    last_messages[message.chat.id] = 'ro;1'


@bot.message_handler()
def get_text(message):
    if message.chat.id not in last_messages:
        bot.send_message(message.chat.id, cmds.get('help'))
        return
    doc, step = last_messages[message.chat.id].split(';')
    if doc == 'ro':
        bot.send_message(message.chat.id, get_ro_new_message(message, int(step), message.chat.id))
        if int(step) == 8:
            file = process_ro_full(forms[message.chat.id]["data"])
            bot.send_document(message.chat.id, open(file, 'rb'))
            last_messages.pop(message.chat.id, None)
            forms.pop(message.chat.id, None)


def get_ro_new_message(msg, step, chat_id) -> str:
    if step == 1:
        forms[chat_id] = {"doc": "ro", "data": {}}
        forms[chat_id]["data"]["mentorJob"] = msg.text
        last_messages[chat_id] = 'ro;2'
        return 'Как зовут вашего наставника?'
    elif step == 2:
        forms[chat_id]["data"]["mentorName"] = msg.text
        last_messages[chat_id] = 'ro;3'
        return 'Какая должность у вашего академического руководителя?'
    elif step == 3:
        forms[chat_id]["data"]["masterJob"] = msg.text
        last_messages[chat_id] = 'ro;4'
        return 'Как зовут вашего академического руководителя?'
    elif step == 4:
        forms[chat_id]["data"]["masterName"] = msg.text
        last_messages[chat_id] = 'ro;5'
        return 'Из какой вы группы?'
    elif step == 5:
        forms[chat_id]["data"]["studentGroup"] = msg.text
        last_messages[chat_id] = 'ro;6'
        return 'Как вас зовут?'
    elif step == 6:
        forms[chat_id]["data"]["studentName"] = msg.text
        last_messages[chat_id] = 'ro;7'
        return 'Как называется ваш проект?'
    elif step == 7:
        forms[chat_id]["data"]["projectName"] = msg.text
        last_messages[chat_id] = 'ro;8'
        return 'Ссылка на ваш проект:'
    elif step == 8:
        forms[chat_id]["data"]["link"] = msg.text
        last_messages[chat_id] = 'ro;9'
        return 'Конвертирую pdf...'


bot.polling()
