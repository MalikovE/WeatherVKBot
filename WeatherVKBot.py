# Weather VKBot, ver. 1.0, author Malikov E.

import vk_api
import pyowm
import random
import time

vk = vk_api.VkApi(token="vk_token")
vk._auth_token()

owm = pyowm.OWM("pyown_token")
show_weather = False

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if body.lower() == "погода":
                show_weather = True
                vk.method("messages.send", {"peer_id": id, "message": "Какой город вас интересует?", 
                    "random_id": random.randint(1, 2147483647)})
            elif show_weather:
                try:
                    show_weather = False
                    observation = owm.weather_at_place(body)
                    w = observation.get_weather()
                    temperature = int(w.get_temperature('celsius')['temp'])
                    vk.method("messages.send", {"peer_id": id, "message": 'В городе ' + body + ' сейчас температура ' + 
                        str(temperature) + ' по Цельсию.', "random_id": random.randint(1, 2147483647)})
                except:
                    vk.method("messages.send", {"peer_id": id, "message": "Город не найден", "random_id": random.randint(1, 2147483647)})
            else:
                vk.method("messages.send", {"peer_id": id, "message": "Команда \"" + str(body.lower()) + "\" не опознана.", 
                    "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        time.sleep(1)

