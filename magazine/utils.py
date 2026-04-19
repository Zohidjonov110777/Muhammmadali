import requests

def send_telegram_message(message):
    token = "SIZNING_BOT_TOKENINGIZ"
    chat_id = "SIZNING_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try: requests.post(url, data=payload)
    except: pass