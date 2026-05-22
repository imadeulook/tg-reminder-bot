import os
import asyncio
import logging
from datetime import datetime
from telegram import Bot
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# ======================
# CONFIG (из GitHub Secrets)
# ======================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

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
# MAIN LOGIC
# ======================

async def main():
    now_local = datetime.now(ZoneInfo("Asia/Bishkek"))
    now_utc = datetime.now(timezone.utc)

    today = now_local.strftime("%d.%m.%y")

    log("========== RUN START ==========")
    log(f"FILE: {os.path.abspath(__file__)}")
    log(f"PID: {os.getpid()}")
    log(f"LOCAL TIME: {now_local}")
    log(f"UTC TIME:   {now_utc}")
    log(f"CHECK DATE: {today}")
    log(f"SCHEDULE KEYS: {list(SCHEDULE.keys())}")

    # ❌ если нет даты — ничего не делаем
    if today not in SCHEDULE:
        log(f"SKIP: no schedule for {today}")
        return

    name = SCHEDULE[today]

    text = (
        f"🚨 *{name} — {today}*\n\n"
        f"⏰ Напоминание"
    )

    try:
        log("SENDING MESSAGE...")

        bot = Bot(token=TOKEN)

        msg = await bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode="Markdown",
            disable_notification=False
        )

        log("PINNING MESSAGE...")

        await bot.pin_chat_message(
            chat_id=CHAT_ID,
            message_id=msg.message_id,
            disable_notification=False
        )

        log(f"SENT OK + PINNED: {text}")
        log(f"MESSAGE_ID: {msg.message_id}")

    except Exception as e:
        log(f"ERROR: {e}")

# ======================
# RUN
# ======================

if __name__ == "__main__":
    asyncio.run(main())