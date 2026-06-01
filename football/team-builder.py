import os
import json
import random
import asyncio
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

DATA_FILE = "football/data.json"


def load_players():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)["players"]


def reset_players():
    with open(DATA_FILE, "w") as f:
        json.dump({"players": []}, f)


def build_teams(players):
    random.shuffle(players)

    team_size = 7
    teams = [players[i:i + team_size] for i in range(0, len(players), team_size)]
    return teams


async def main():
    bot = Bot(token=TOKEN)

    players = load_players()

    if len(players) < 7:
        await bot.send_message(CHAT_ID, "❌ Недостаточно игроков (минимум 7)")
        return

    teams = build_teams(players)

    text = "⚽ Команды сформированы:\n\n"

    for i, team in enumerate(teams, 1):
        text += f"Команда {i}:\n" + "\n".join([f"- {p}" for p in team]) + "\n\n"

    await bot.send_message(CHAT_ID, text)

    reset_players()


if __name__ == "__main__":
    asyncio.run(main())