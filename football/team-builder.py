import os
import json
import asyncio
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

PLAYERS_FILE = "data/players.json"
RATINGS_FILE = "data/ratings.json"

# ======================
# TEST CONFIG
# ======================

TEAM_COUNT = 2   # 3 команды
TEAM_SIZE = 3    # по 3 игрока (TEST MODE)
SUBS = 1  # кол-во запасных в команде (TEST MODE)

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

    main_count = TEAM_COUNT * TEAM_SIZE

    main = players[:main_count]
    subs_pool = players[main_count:]

    # основные команды
    teams = [[] for _ in range(TEAM_COUNT)]
    power = [0] * TEAM_COUNT

    for i, p in enumerate(main):
        idx = i % TEAM_COUNT

        teams[idx].append(p)
        power[idx] += p["power"]

    # распределяем запасных (round robin)
    SUB_LIMIT = 3
    subs_added = [0] * TEAM_COUNT

    for p in subs_pool:
        # ищем команду с минимальным запасом
        idx = min(range(TEAM_COUNT), key=lambda i: subs_added[i])

        if subs_added[idx] >= SUB_LIMIT:
            continue  # лимит 3 замены

        teams[idx].append(p)
        power[idx] += p["power"]
        subs_added[idx] += 1

    return teams, power


# ======================
# MAIN
# ======================

async def main():

    bot = Bot(token=TOKEN)

    players = load_players()
    ratings = load_ratings()

    needed = TEAM_COUNT * TEAM_SIZE

    if len(players) < needed:
        await bot.send_message(
            CHAT_ID,
            f"❌ Нужно минимум {needed} игроков (сейчас {len(players)})"
        )
        return

    enriched = enrich(players, ratings)

    teams, power, = build_teams(enriched)  # subs больше не используем

    text = "⚽ <b>Команды сформированы (TEST MODE)</b>\n\n"

    colors = ["🔵", "🟠", "🟢"]

    SUBS_PER_TEAM = SUBS  # сколько запасных в каждой команде

    for i, team in enumerate(teams):
        color = colors[i] if i < len(colors) else "⚽"

        # сортируем по силе
        sorted_team = sorted(team, key=lambda x: x["power"], reverse=True)

        main_players = sorted_team[:-SUBS_PER_TEAM]
        subs = sorted_team[-SUBS_PER_TEAM:]

        text += f"{color} Команда {i+1}\n"

        for p in main_players:
            text += f"• {p['name']}\n"

        if subs:
            text += "    ⚪ Запасные:\n"
            for p in subs:
                text += f"• {p['name']}\n"

        text += "\n"

    await bot.send_message(
        CHAT_ID,
        text,
        parse_mode="HTML"
    )

    reset_players()

if __name__ == "__main__": asyncio.run(main())