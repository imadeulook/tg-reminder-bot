import asyncio
import logging
import os
from datetime import datetime
from telegram import Bot

# ======================
# CONFIG
# ======================

LOG_FILE = "/Users/Timur_Akkulakov/Python/tg_bot.log"

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SCHEDULE = {
    "20.05.26": "Элдик сегодня стирает манишки",
    "27.05.26": "Арис сегодня стирает манишки",
    "03.06.26": "Авта сегодня стирает манишки",
    "10.06.26": "Тарик сегодня стирает манишки",
    "17.06.26": "Эсен сегодня стирает манишки",
    "24.06.26": "Нурс сегодня стирает манишки",
    "01.07.26": "Аза Т сегодня стирает манишки",
    "08.07.26": "Адик сегодня стирает манишки",
    "15.07.26": "Аза Биг сегодня стирает манишки",
    "22.07.26": "Тилек сегодня стирает манишки",
    "29.07.26": "Руга сегодня стирает манишки",
    "05.08.26": "Батя сегодня стирает манишки",
    "12.08.26": "Ильяс сегодня стирает манишки",
    "19.08.26": "Беля А сегодня стирает манишки",
    "26.08.26": "Мастер сегодня стирает манишки",
    "02.09.26": "Тала сегодня стирает манишки",
    "09.09.26": "Мерз сегодня стирает манишки",
    "16.09.26": "СЕО сегодня стирает манишки",
    "23.09.26": "Сэм сегодня стирает манишки",
    "30.09.26": "Айба сегодня стирает манишки",
    "07.10.26": "Сочи сегодня стирает манишки",
    "14.10.26": "Ди сегодня стирает манишки",
    "21.10.26": "Мазя сегодня стирает манишки",
    "28.10.26": "Чика сегодня стирает манишки",
    "04.11.26": "Кудя сегодня стирает манишки",
    "11.11.26": "Коена сегодня стирает манишки",
    "18.11.26": "Белек Дж сегодня стирает манишки",
    "25.11.26": "Данчик сегодня стирает манишки",
    "02.12.26": "Газнач сегодня стирает манишки",
    "09.12.26": "Тимс сегодня стирает манишки",
    "16.12.26": "Володя сегодня стирает манишки",
    "23.12.26": "Дас сегодня стирает манишки"
}

# ======================
# LOGGING
# ======================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def log(msg: str):
    logging.info(msg)

# ======================
# DIAGNOSTICS
# ======================

log(f"FILE_PATH = {os.path.abspath(__file__)}")
log(f"PID = {os.getpid()}")

# ======================
# MAIN LOGIC
# ======================

async def main():
    today = datetime.now().strftime("%d.%m.%y")

    log(f"TODAY = {today}")

    if today not in SCHEDULE:
        log("NO TASK TODAY — EXIT")
        return

    name = SCHEDULE[today]
    date = today

    text = f"🚨 *{name} — {date}*\n\n⏰ Сегодня по расписанию"

    try:
        bot = Bot(token=TOKEN)

        msg = await bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode="Markdown",
            disable_notification=False
        )

        await bot.pin_chat_message(
            chat_id=CHAT_ID,
            message_id=msg.message_id
        )

        log(f"SENT + PINNED: {text}")

    except Exception as e:
        log(f"ERROR: {e}")

# ======================
# RUN
# ======================

if __name__ == "__main__":
    asyncio.run(main())