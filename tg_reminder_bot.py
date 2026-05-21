import os
import asyncio
import logging
from datetime import datetime
from telegram import Bot

# ======================
# CONFIG (из GitHub Secrets)
# ======================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ======================
# LOGGING (GitHub Actions читает stdout)
# ======================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

log = logging.info

# ======================
# SCHEDULE (твои даты)
# ======================

SCHEDULE = {
    "20.05.26": "Элдик",
    "27.05.26": "Арис",
    "03.06.26": "Авта",
    "10.06.26": "Тарик",
    "17.06.26": "Эсен",
    "24.06.26": "Нурс",
    "01.07.26": "Аза Т",
    "08.07.26": "Адик",
    "15.07.26": "Аза Биг",
    "22.07.26": "Тилек",
    "29.07.26": "Руга",
    "05.08.26": "Батя",
    "12.08.26": "Ильяс",
    "19.08.26": "Беля А",
    "21.05.26": "Мастер сегодня стирает манишки",
    "02.09.26": "Тала",
    "09.09.26": "Мерз",
    "16.09.26": "СЕО",
    "23.09.26": "Сэм",
    "30.09.26": "Айба",
    "07.10.26": "Сочи",
    "14.10.26": "Ди",
    "21.10.26": "Мазя",
    "28.10.26": "Чика",
    "04.11.26": "Кудя",
    "11.11.26": "Коена",
    "18.11.26": "Белек Дж",
    "25.11.26": "Данчик",
    "02.12.26": "Газнач",
    "09.12.26": "Тимс",
    "16.12.26": "Володя",
    "23.12.26": "Дас"
}

# ======================
# MAIN LOGIC
# ======================

async def main():
    now = datetime.now()
    today = now.strftime("%d.%m.%y")
    current_time = now.strftime("%H:%M")

    log(f"FILE STARTED")
    log(f"TODAY = {today}")
    log(f"TIME = {current_time}")

    # ❌ если нет даты — ничего не делаем
    if today not in SCHEDULE:
        log(f"SKIP: no schedule for {today}")
        return

    name = SCHEDULE[today]

    text = (
        f"🚨 *{name} — {today}*\n\n"
        f"⏰ Напоминание (18:20)"
    )

    try:
        bot = Bot(token=TOKEN)

        msg = await bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode="Markdown",
            disable_notification=False
        )

        log(f"SENT: {text}")
        log(f"MESSAGE_ID: {msg.message_id}")

    except Exception as e:
        log(f"ERROR: {e}")

# ======================
# RUN
# ======================

if __name__ == "__main__":
    asyncio.run(main())