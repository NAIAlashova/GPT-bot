HOME_DIR = '/home/student/GPT-bot'
LOGS = f'{HOME_DIR}/log.txt'
DB_FILE = f'{HOME_DIR}/messages.db'

IAM_TOKEN_PATH = f'{HOME_DIR}/creds/iam_token.txt'
FOLDER_ID_PATH = f'{HOME_DIR}/creds/folder_id.txt'
BOT_TOKEN_PATH = f'{HOME_DIR}/creds/bot_token.txt'

query1 = '''CREATE TABLE IF NOT EXISTS 'Requests' (

user_id INTEGER, 
role TEXT,
contents TEXT,
tokens INTEGER,
blocks INTEGER);'''
#id INTEGER PRIMARY KEY,
hi = 'Привет. Я - бот и твой помощник. \nC помощью команд /tts и /stt ты можешь озвучить или перевести в текст своё сообщение соответственно. \nЕсли хочешь, чтобы я ответил на твой вопрос, просто пиши его или отправляй голосовое с ним. Я пойму'
help = 'Что случилось? Если я тебя не понимаю, сорри. Такое бывает, просто спроси по-другому. Но может быть, это я сломался. Тогда тебе придётся подождать, пока меня не исправят.'
about = 'Я - бот-помощник. Меня подключили к нейросети, и теперь я могу общаться с тобой как человек. Даже присылать голосовые.'
