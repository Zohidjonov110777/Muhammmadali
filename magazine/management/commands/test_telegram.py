from django.core.management.base import BaseCommand
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Test Telegram bot connection'

    def handle(self, *args, **options):
        self.stdout.write('Telegram bo\'t testlamoq...\n')
        
        # Settings qiymatlari
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        
        self.stdout.write(f'Token: {token[:20]}...')
        self.stdout.write(f'Chat ID: {chat_id}\n')
        
        # Test xabar
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": "✅ Test xabar - Telegram bot ishlayapti!"
        }
        
        try:
            response = requests.post(url, data=payload, timeout=5)
            result = response.json()
            
            if result.get('ok'):
                self.stdout.write(self.style.SUCCESS('✅ Xabar yuborildi!'))
                self.stdout.write(f'Response: {result}')
            else:
                self.stdout.write(self.style.ERROR('❌ Xato!'))
                self.stdout.write(f'Error: {result}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ulanishda xato: {e}'))
