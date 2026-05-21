import os
import asyncio
import logging
from datetime import datetime, timezone
from telegram import Bot

# ======================
# CONFIG
# ======================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ======================
# LOGGING
# ======================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

log = logging.info

# ======================
# SCHEDULE
# ======================

SCHEDULE = {
    "21.05.26": "Мастер сегодня стирает манишки",
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
# MAIN
# ======================

async def send_message():
    now_local = datetime.now()
    now_utc = datetime.now(timezone.utc)

    today = now_local.strftime("%d.%m.%y")

    log("========== RUN START ==========")
    log(f"FILE: {os.path.abspath(__file__)}")
    log(f"PID: {os.getpid()}")
    log(f"LOCAL TIME: {now_local}")
    log(f"UTC TIME:   {now_utc}")
    log(f"CHECK DATE: {today}")
    log(f"SCHEDULE KEYS: {list(SCHEDULE.keys())}")

    # ❌ если даты нет — выходим
    if today not in SCHEDULE:
        log(f"SKIP: no schedule for {today}")
        log("========== RUN END ==========")
        return

    name = SCHEDULE[today]

    text = (
        f"🚨 *{name} — {today}*\n\n"
        f"⏰ Напоминание (18:20)"
    )

    try:
        log("SENDING MESSAGE...")

        bot = Bot(token=TOKEN)

        msg = await bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode="Markdown"
        )

        log(f"SENT OK | message_id={msg.message_id}")

    except Exception as e:
        log(f"ERROR: {e}")

    log("========== RUN END ==========")

# ======================
# ENTRY
# ======================

if __name__ == "__main__":
    asyncio.run(send_message())