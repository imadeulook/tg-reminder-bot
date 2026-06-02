import os
import json
import asyncio
import logging
import subprocess
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
# ADMINS
# ======================

ADMINS = [790870831]  # <-- твой ID сюда

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# ======================
# STATE
# ======================

REGISTRATION_OPEN = False


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
        json.dump(data, f, indent=2)


def reset_players():
    save_data({"players": []})


# ======================
# HELP
# ======================

async def handle_help(chat_id):
    text = (
        "⚽ <b>Football Bot</b>\n\n"

        "👤 Игроки\n"
        "/ingame — записаться\n"
        "/out — выйти\n"
        "/status — список игроков\n\n"

        "🟢 Регистрация (admin)\n"
        "/openvote — начать набор\n"
        "/lockvote — закрыть набор\n\n"

        "🚀 Система (admin)\n"
        "/push — сохранить в Git\n\n"

        "🆔 Инфо\n"
        "/id — твой ID\n"
        "/help — команды"
    )

    await bot.send_message(chat_id, text, parse_mode="HTML")


# ======================
# HANDLER
# ======================

async def handle(update: dict):
    if "message" not in update:
        return

    msg = update["message"]
    text = msg.get("text", "")
    chat_id = msg["chat"]["id"]
    user = msg["from"]

    user_id = user["id"]
    name = user.get("first_name", "player")

    data = load_data()
    players = data["players"]

    global REGISTRATION_OPEN

    # ======================
    # ROUTER
    # ======================

    match text:

        # ---------------- HELP ----------------
        case "/help":
            await handle_help(chat_id)

        # ---------------- ID ----------------
        case "/id":
            await bot.send_message(chat_id, f"Your ID: {user_id}")

        # ---------------- STATUS ----------------
        case "/status":
            names = "\n".join([f"• {p['name']}" for p in players]) or "пусто"
            await bot.send_message(chat_id, f"👥 {len(players)} игроков\n\n{names}")

        # ---------------- INGAME ----------------
        case "/ingame":
            if not REGISTRATION_OPEN:
                await bot.send_message(chat_id, "❌ регистрация закрыта")
                return

            if any(p["id"] == user_id for p in players):
                await bot.send_message(chat_id, "⚠️ ты уже в игре")
                return

            players.append({"id": user_id, "name": name})
            save_data({"players": players})

            await bot.send_message(chat_id, f"✅ {name} добавлен")

        # ---------------- OUT ----------------
        case "/out":
            players = [p for p in players if p["id"] != user_id]
            save_data({"players": players})

            await bot.send_message(chat_id, "👋 ты вышел")

        # ======================
        # ADMIN COMMANDS
        # ======================

        # ---------------- OPENVOTE ----------------
        case "/openvote":
            if not is_admin(user_id):
                await bot.send_message(chat_id, "⛔ нет прав")
                return

            reset_players()
            REGISTRATION_OPEN = True

            await bot.send_message(
                chat_id,
                "🟢 НОВОЕ ГОЛОСОВАНИЕ\n\n"
                "👥 список очищен\n"
                "👉 /ingame чтобы войти"
            )

        # ---------------- LOCKVOTE ----------------
        case "/lockvote":
            if not is_admin(user_id):
                await bot.send_message(chat_id, "⛔ нет прав")
                return

            REGISTRATION_OPEN = False

            await bot.send_message(
                chat_id,
                f"🔒 закрыто\n👥 игроков: {len(players)}"
            )

        # ---------------- PUSH ----------------
        case "/push":
            if not is_admin(user_id):
                await bot.send_message(chat_id, "⛔ нет прав")
                return

            try:
                repo = BASE_DIR

                subprocess.run(["git", "add", DATA_FILE], cwd=repo, check=True)
                subprocess.run(["git", "commit", "-m", "update players"], cwd=repo, check=True)
                subprocess.run(["git", "push", "origin", "dev"], cwd=repo, check=True)

                await bot.send_message(chat_id, "🚀 pushed")

            except Exception as e:
                await bot.send_message(chat_id, f"❌ git error: {e}")

        # ---------------- DEFAULT ----------------
        case _:
            pass


# ======================
# POLLING LOOP
# ======================

async def run():
    offset = 0
    log("🚀 FOOTBALL BOT STARTED")

    while True:
        try:
            updates = await bot.get_updates(offset=offset, timeout=30)

            for u in updates:
                offset = u.update_id + 1
                await handle(u.to_dict())

        except Exception as e:
            log(f"ERROR: {e}")

        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(run())