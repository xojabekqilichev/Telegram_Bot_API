import time
import requests
from asosiy import TOKEN
BASE_URL = TOKEN

class Bot:
    def __init__(self, token):
        self.BASE_URL = f"https://api.telegram.org/bot{token}"
        self.offset = None

    def get_me(self):
        get_me_url = f"{self.BASE_URL}/getMe"
        response = requests.get(get_me_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("error")

    def get_updates(self):
        get_updates_url = f"{self.BASE_URL}/getUpdates"
        data = {
            "offset": self.offset, 
            "limit": 5}
        response = requests.get(get_updates_url, params=data)
        if response.status_code == 200:
            return response.json()["result"]
        else:
            raise Exception("error")

    def send_message(self, chat_id, text):
        get_message_url = f"{self.BASE_URL}/sendMessage"
        params = {
            "chat_id": chat_id, 
            "text": text
            }
        response = requests.get(get_message_url, params=params)

    def send_photo(self, chat_id, photo):
        get_photo_url = f"{self.BASE_URL}/sendPhoto"
        params = {
            "chat_id": chat_id, 
            "photo": photo
            }
        response = requests.get(get_photo_url, params=params)

    def send_audio(self, chat_id, audio):
        get_audio = f"{self.BASE_URL}/sendAudio"
        params = {
            "chat_id": chat_id, 
            "audio": audio
            }
        response = requests.get(get_audio, params=params)

    def send_voice(self, chat_id, voice):
        get_voice =  f"{self.BASE_URL}/sendVoice"
        params = {
            "chat_id": chat_id, 
            "voice": voice
            }
        response = requests.get(get_voice, params=params)

    def send_video(self, chat_id, video):
        get_video = f'{self.BASE_URL}/sendVideo'
        params = {
            "chat_id": chat_id, 
            "video_id": video
            }
        response = requests.get(get_video, params=params)
        return response
    def send_location(self, chat_id, latitude, longitude):
        send_location_url = f'{self.BASE_URL}/sendLocation'
        params = {
            'chat_id'  : chat_id,
            'latitude' : latitude,
            'longitude': longitude
        }
        response= requests.get(send_location_url, params=params)
    def start_polling(self):
        while True:
            updates = self.get_updates()
            time.sleep(0.1)
            for update in updates:
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    text = message.get("text")
                    if message:
                        chat_id = message["chat"]["id"]
                    
                        if "text" in message:
                            self.send_message(chat_id, message["text"])
                    
                        elif "photo" in message:
                            self.send_photo(chat_id, message["photo"][-1]["file_id"])
                        
                        elif "audio" in message:
                            self.send_audio(chat_id, message["audio"]["file_id"])
                        
                        elif "video" in message:
                            self.send_video(chat_id, message["video"]["file_id"])
                        location = message.get("location")
                        if "location" in message:
                            latitude = location['latitude']
                            longitude = location['longitude']
                            self.send_location(
                                chat_id=chat_id,
                                latitude=latitude,
                                longitude=longitude
                                )

                self.offset = update["update_id"] + 1


bot = Bot(TOKEN)
bot.start_polling()