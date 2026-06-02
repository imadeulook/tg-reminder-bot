import os
import json
import asyncio
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

PLAYERS_FILE = "data/players.json"
RATINGS_FILE = "data/ratings.json"


# ======================
# LOADERS
# ======================

def load_players():
    if not os.path.exists(PLAYERS_FILE):
        return []

    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("players", [])


def load_ratings():
    if not os.path.exists(RATINGS_FILE):
        return {}

    with open(RATINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def reset_players():
    with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"players": []}, f, indent=2, ensure_ascii=False)


# ======================
# RATING ENGINE
# ======================

def calc_power(grade: str, score: float):
    bonus = {
        "A": 3,
        "B": 1,
        "C": 0,
        "D": -1
    }
    return float(score) + bonus.get(grade.upper(), 0)


def enrich(players, ratings):
    enriched = []

    for p in players:
        r = ratings.get(str(p["id"]))

        if r:
            power = calc_power(r["grade"], r["score"])
            grade = r["grade"]
        else:
            power = 20  # fallback
            grade = "C"

        enriched.append({
            "id": p["id"],
            "name": p["name"],
            "power": power,
            "grade": grade
        })

    return sorted(enriched, key=lambda x: x["power"], reverse=True)


# ======================
# TEAM BUILDING
# ======================

def build_teams(players):

    main = players[:21]   # 3 команды по 7
    subs = players[21:]   # запасные (до 3)

    teams = [[], [], []]
    power = [0, 0, 0]

    for i, p in enumerate(main):
        idx = i % 3

        teams[idx].append(p)
        power[idx] += p["power"]

    return teams, power, subs


# ======================
# MAIN
# ======================

async def main():

    bot = Bot(token=TOKEN)

    players = load_players()
    ratings = load_ratings()

    if len(players) < 21:
        await bot.send_message(
            CHAT_ID,
            f"❌ Нужно минимум 21 игрок (сейчас {len(players)})"
        )
        return

    enriched = enrich(players, ratings)

    teams, power, subs = build_teams(enriched)

    text = "⚽ <b>Команды сформированы</b>\n\n"

    for i, team in enumerate(teams, 1):
        text += f"🔵 Команда {i} ({round(power[i-1],1)})\n"
        for p in team:
            text += f"• {p['name']} ({p['grade']} | {round(p['power'],1)})\n"
        text += "\n"

    if subs:
        text += "🟡 Запасные:\n"
        for p in subs:
            text += f"• {p['name']} ({p['grade']} | {round(p['power'],1)})\n"

    await bot.send_message(
        CHAT_ID,
        text,
        parse_mode="HTML"
    )

    reset_players()


if __name__ == "__main__":
    asyncio.run(main())