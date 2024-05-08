import telebot
import logging
import config
from creds import get_bot_token
from ds import execute_query, count_all_symbol, count_all_blocks
from GPT import ask_gpt, count_tokens, to_speech, to_text

bot = telebot.TeleBot(get_bot_token())
logging.basicConfig(level=logging.DEBUG, filename='log.txt', format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")
execute_query(config.query1)
def ask(text, message, type):
    ans = ask_gpt(text)
    tokens = count_tokens(ans)
    blocks = tokens
    if type == 'текст':
        blocks = 0
    execute_query(f'''INSERT INTO Requests VALUES ({message.from_user.id}, 'assistent', '{message.text}', {tokens}, {blocks}) ;''')
    return ans
def right(message):
    if '/' in message.text:
        if 'logging' in message.text:
            handle_logging(message)
        elif 'about' in message.text:
            handle_about(message)
        elif 'help' in message.text:
            handle_help(message)
        elif 'start' in message.text:
            handle_start(message)
        else:
            bot.send_message(message.chat.id, 'Непонятный запрос. Попробуйте пожалуйста заново.')
    else:
       pass
def validators(message, type):
    if type == 'текст':
        if count_all_symbol(message.from_user.id) > 5000:
            return False
        else:
            return True
    else:
        if count_all_blocks(message.from_user.id) > 120:
            return False
        else:
            return True
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, config.hi)
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, config.help)
@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.chat.id, config.about)
@bot.message_handler(commands=['logging'])
def handle_logging(message):
    bot.send_document(message.chat.id, 'log.txt')
@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь следующим сообщением текст, чтобы я его озвучил!')
    bot.register_next_step_handler(message, tts)
def tts(message):
    user_id = message.from_user.id
    text = message.text
    if message.content_type != 'text':
        bot.send_message(user_id, 'Отправь текстовое сообщение')
        return
    if not validators(message, 'голос'):
        bot.send_message(message.chat.id, 'У вас закончились блоки для голосовых сообщений. Попробуйте написать текстом.')
        return
    p, ans = to_speech(text)
    if p:
        with open("output.ogg", "wb") as audio:
            audio.write(ans)
        bot.send_voise(message.chat.id, ans)
        execute_query(f'''INSERT INTO Requests VALUES ({message.from_user.id}, 'user', '{text}', {0}, {count_tokens(text)});''')
    else:
        bot.send_message(message.chat.id, 'Произошла какая-то ошибка. Попробуй заново.')
        logging.error('Произошла ошибка ' + ans)
@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь голосовое сообщение, чтобы я его распознал!')
    bot.register_next_step_handler(message, stt)
def stt(message):
    if not message.voice:
        return
    if not validators(message, 'голос'):
        bot.send_message(message.chat.id, 'У вас закончились блоки для голосовых сообщений. Попробуйте написать текстом.')
        return
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    p, ans = to_text(file)
    if p:
        bot.send_voise(message.chat.id, ans)
        execute_query(f'''INSERT INTO Requests VALUES ({message.from_user.id}, 'user', '{ans}', {0}, {int(message.voice.duration/15)});''')
    else:
        bot.send_message(message.chat.id, 'Произошла какая-то ошибка. Попробуй заново.')
        logging.error('Произошла ошибка ' + ans)
@bot.message_handler(content_types=['text'])
def writing(message):
    right(message)
    if not validators(message, 'текст'):
        bot.send_message(message.chat.id, 'У вас закончились токены.')
        return
    blok_ask = 0
    token_ask = count_tokens(message.text)
    execute_query(f'''INSERT INTO Requests VALUES ({message.from_user.id}, 'user', '{message.text}', {token_ask}, {blok_ask}) ;''')
    ans = ask(message.text, message, 'текст')
    bot.send_message(message.chat.id, ans)
@bot.message_handler(content_types=['audio'])
def speech(message):
    if not validators(message, 'голос'):
        bot.send_message(message.chat.id, 'У вас закончились блоки для голосовых сообщений. Попробуйте написать текстом.')
        return
    blok_ask = int(message.voice.duration/15)
    p, text = to_text(message.text)
    token_ask = count_tokens(text)
    if p:
        ans = ask(text, message, 'голос')
        p, ans = to_speech(ans)
        if p:
            with open("output.ogg", "wb") as audio:
                audio.write(ans)
            bot.send_voise(message.chat.id, ans)
            execute_query(f'''INSERT INTO Requests VALUES ({message.from_user.id}, 'user', '{text}', {token_ask}, {blok_ask});''')
        else:
            bot.send_message(message.chat.id, 'Произошла какая-то ошибка. Попробуй заново.')
            logging.error('Произошла ошибка ' + ans)
    else:
        logging.error(text)
        bot.send_message(message.chat.id, 'Произошла какая-то ошибка. Попробуй заново.')

bot.infilly_polling()
