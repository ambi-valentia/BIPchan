from django.shortcuts import render
import json
import os

import requests
from django.http import JsonResponse
from django.views import View

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = '1450225782:AAFJXFk4bfWSPu1KeoO78RQZkChICMcEQH8'

# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
class TelegramBot(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        try:
            t_message = t_data["message"]
            t_chat = t_message["chat"]
            t_id = int(t_chat["id"])
            text = t_message["text"]
        except:
            print("Unknown message type!")
            return JsonResponse({"ok": "POST request processed"})

        text = text.lstrip("/")
        print(text)
        if text == "getid":
            self.send_message(f"Your ID is {t_id}", t_chat["id"])
        else:
            msg = "Unknown command"
            self.send_message(msg, t_chat["id"])

        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )


# Call     TelegramBot.send_notification("google.com", 200020353)
    
    @staticmethod
    def send_notification(link, chat_id, username = None, thread = None):
        msg = f"Hello,"
        if username : msg += f" {username},"
        msg += " a new post"
        if thread : msg += f" with thread {thread}"
        msg += f" is available here: {link}"
        data = {
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )