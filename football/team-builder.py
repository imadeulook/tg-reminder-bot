import json
import os
import random
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DATA_FILE = "data/players.json"


def load_players():
    with open(DATA_FILE, "r") as f:
        return json.load(f)["players"]


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })


def build_teams(players):
    random.shuffle(players)
    return [players[i:i+7] for i in range(0, len(players), 7)]


def main():
    players = load_players()

    if len(players) < 7:
        send_message(f"❌ Недостаточно игроков: {len(players)}")
        return

    teams = build_teams(players)

    text = f"⚽ Всего игроков: {len(players)}\n\n"

    for i, team in enumerate(teams, 1):
        text += f"🔵 Команда {i}\n"
        text += "\n".join([f"• {p}" for p in team])
        text += "\n\n"

    send_message(text)


if __name__ == "__main__":
    main()