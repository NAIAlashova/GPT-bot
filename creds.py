import json
import logging
import time
from datetime import datetime
import requests
from config import LOGS, IAM_TOKEN_PATH, FOLDER_ID_PATH, BOT_TOKEN_PATH

logging.basicConfig(filename='log.txt', level=logging.INFO, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")
def create_new_token():
    metadata_url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {"Metadata-Flavor": "Google"}
    try:
        response = requests.get(metadata_url, headers=headers)
        if response.status_code == 200:
            logging.info("Получен новый iam_token")
            # Надо написать программу, перезаписывающую iam token в файл
            return response.json()
        else:
            logging.error(f"Ошибка получения iam_token. Статус-код: {response.status_code}")
    except Exception as e:
        logging.error(f"Ошибка получения iam_token: {e}")
def get_creds():
    try:
        with open(IAM_TOKEN_PATH, 'r') as f:
            expiration = datetime.strptime(json.load(f)["expires_at"][:26], "%Y-%m-%dT%H:%M:%S.%f")
        if expiration < datetime.now():
            logging.info("Срок годности iam_token истёк")
            create_new_token()
    except:
        create_new_token()
    with open(IAM_TOKEN_PATH, 'r') as f:
        # iam_token = json.load(f)["access_token"]
        iam_token = f.read().strip()
    with open(FOLDER_ID_PATH, 'r') as f:
        folder_id = f.read().strip()
    return iam_token, folder_id
def get_bot_token():
    with open(BOT_TOKEN_PATH, 'r') as f:
        return f.read().strip()
