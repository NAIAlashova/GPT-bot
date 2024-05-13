import requests
import logging
from creds import get_creds

logging.basicConfig(level=logging.DEBUG, filename='log.txt', format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")
def to_text(voice):
    iam_token, folder_id = get_creds()
    params = "&".join(["topic=general", f"folderId={folder_id}", "lang=ru-RU" ])
    headers = {'Authorization': f'Bearer {iam_token}',}
    response = requests.post(f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}", headers=headers, data=voice)
    decoded_data = response.json()
    ans = decoded_data.get("result")
    if decoded_data.get("error_code") is None:
        return True, ans
    else:
        return False, decoded_data.get("error_code")
def to_speech(text):
    iam_token, folder_id = get_creds()
    headers = {'Authorization': f'Bearer {iam_token}',}
    data = {
        'text': text,
        'lang': 'ru-RU',  # язык текста
        'voice': 'filipp',  # голос Филиппа
        'folderId': folder_id,}
    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)
    if response.status_code == 200:
        return True, response.content
    else:
        logging.error('Произошла ошибка ' + str(response.status_code))
        return False, ''

def ask_gpt(collection):
    url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    iam_token, folder_id = get_creds()
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'}
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 200},
        "messages": []}
    data["messages"].append({
        "role": 'user',
        "text": collection})
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            result = f"Status code {response.status_code}."
            return result
        result = response.json()['result']['alternatives'][0]['message']['text']
    except Exception:
        result = "Произошла непредвиденная ошибка. Подробности см. в журнале."
        logging.basicConfig(level=logging.DEBUG, filename='log.txt')
    return result

def count_tokens(text):
    iam_token, folder_id = get_creds()
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'}
    len_tokens = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
        json={"modelUri": f"gpt://{folder_id}/yandexgpt/latest", "text": text},
        headers=headers)
    return len(len_tokens.json()['tokens'])
