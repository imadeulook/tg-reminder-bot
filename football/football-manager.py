import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

DATA_FILE = "football/data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"players": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# /football
async def football(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚽ Я играю", callback_data="join")]
    ]

    await update.message.reply_text(
        "⚽ Игра открыта!\nНажми кнопку чтобы записаться",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# кнопка
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    data = load_data()

    # защита от дубля
    if user.id not in data["players"]:
        data["players"].append(user.id)
        save_data(data)
        await query.edit_message_text(f"✅ {user.first_name} записан")
    else:
        await query.answer("Ты уже в игре", show_alert=True)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("football", football))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == "__main__":
    main()