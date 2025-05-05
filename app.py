import os
from flask import Flask, request
import openai
import requests
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    data = json.loads(body)

    user_message = data["events"][0]["message"]["text"]
    user_id = data["events"][0]["source"]["userId"]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    reply_text = response["choices"][0]["message"]["content"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "to": user_id,
        "messages": [{"type": "text", "text": reply_text}]
    }
    requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=body)

    return "OK"
