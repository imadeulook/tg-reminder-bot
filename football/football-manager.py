import os
import json
import asyncio
import logging
from telegram import Bot

# ======================
# CONFIG
# ======================

TOKEN = "1322219909:AAG13Qfr7GrYqK8nWYUtsd79gAE6AfadL0E"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.normpath(os.path.join(BASE_DIR, "..", "data", "players.json"))

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

logging.basicConfig(level=logging.INFO)
log = logging.info

bot = Bot(token=TOKEN)

# ======================
# STORAGE
# ======================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"players": []}

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"players": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ======================
# INGAME LOGIC
# ======================

async def handle_update(update: dict):
    log(f"UPDATE: {update}")

    if "message" not in update:
        return

    msg = update["message"]
    text = msg.get("text", "")
    chat_id = msg["chat"]["id"]

    user = msg["from"]

    # ---------------- /football ----------------
    if text == "/football":
        data = load_data()
        players = data["players"]

        names = "\n".join([f"• {p['name']}" for p in players])

        text_msg = (
            "⚽ <b>Регистрация открыта</b>\n\n"
            f"👥 Уже в игре: {len(players)}\n\n"
            f"{names if names else 'Пока никого'}\n\n"
            "👉 Напиши /ingame чтобы записаться"
        )

        await bot.send_message(
            chat_id=chat_id,
            text=text_msg,
            parse_mode="HTML"
        )

    # ---------------- /ingame ----------------
    elif text == "/ingame":
        data = load_data()
        players = data["players"]

        player = {
            "id": user["id"],
            "name": user.get("first_name", "unknown")
        }

        # проверка дубля
        if any(p["id"] == player["id"] for p in players):
            await bot.send_message(chat_id, "⚠️ Ты уже в игре")
            return

        players.append(player)
        data["players"] = players
        save_data(data)

        names = "\n".join([f"• {p['name']}" for p in players])

        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"✅ {player['name']} записался!\n\n"
                f"👥 Всего игроков: {len(players)}\n\n"
                f"{names}"
            )
        )


# ======================
# POLLING
# ======================

async def run():
    offset = 0
    log("🚀 BOT STARTED")

    while True:
        try:
            updates = await bot.get_updates(offset=offset, timeout=30)

            for u in updates:
                offset = u.update_id + 1
                await handle_update(u.to_dict())

        except Exception as e:
            log(f"ERROR: {e}")

        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(run())