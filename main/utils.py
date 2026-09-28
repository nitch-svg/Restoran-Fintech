from django.conf import settings
import requests as sorov

def send_receipt_tg(message):
    token = settings.TG_TOKEN
    user_id=8887471601
    message=message
    
    url=f"https://api.telegram.org/bot{token}/sendMessage?" \
        f"chat_id={user_id}&text={message}&parse_mode=HTML"
    
    
    sorov.get(url)