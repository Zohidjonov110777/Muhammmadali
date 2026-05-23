import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
from httpx import post, get

TELEGRAM_BOT_TOKEN = "8546684735:AAESnnWTxhNZ3Ft8QxJqK7J7s2buuVNaYDI"



def send_telegram_message(message):
    """
    Telegramga oddiy xabar yuborish
    """
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        response = requests.post(url, data=payload, timeout=10)

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        result = response.json()

        return result.get("ok", False)

    except Exception as e:
        print("❌ Telegram error:", e)
        logger.error(f"Telegram error: {e}", exc_info=True)
        return False



def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = get(url, params=params)
    print(response.text, response.status_code)



def send_order_notification(order, cart_items):
    """
    Buyurtma haqida Telegramga yuborish
    """
    try:
        items_text = ""

        for item in cart_items:
            product = item.get("product")

            name = product.name if product else "Noma'lum"
            qty = item.get("quantity", 0)
            price = item.get("price", 0)
            total = item.get("total_price", 0)

            items_text += f"• {name}\n  {qty} x {price} = {total} so'm\n\n"

        if not items_text:
            items_text = "Mahsulot yo'q"

        message = f"""
🛒 <b>YANGI BUYURTMA</b>

👤 Ism: {order.full_name}
📞 Telefon: {order.phone}
📍 Manzil: {order.address}

📦 Mahsulotlar:
{items_text}

💰 Jami: {order.total_price} so'm
"""

        return send_telegram_message(message)

    except Exception as e:
        print("❌ Order notification error:", e)
        return False