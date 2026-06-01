import json
import os
from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

DATA_FILE = "data/players.json"


# --------------------
# STORAGE
# --------------------
def load_players():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)["players"]


def save_players(players):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump({"players": players}, f, ensure_ascii=False, indent=2)


# --------------------
# UI
# --------------------
def keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⚽ Буду", callback_data="football_join"),
            InlineKeyboardButton(text="❌ Не буду", callback_data="football_leave")
        ]
    ])


# --------------------
# HANDLERS
# --------------------
def register_handlers(dp):

    @dp.message(Command("football"))
    async def football(message: types.Message):
        players = load_players()

        text = (
            "⚽ <b>Футбол регистрация</b>\n\n"
            f"Игроков: {len(players)}\n\n"
        )

        if players:
            text += "\n".join([f"• {p}" for p in players])

        await message.answer(text, reply_markup=keyboard(), parse_mode="HTML")


    @dp.callback_query(F.data == "football_join")
    async def join(call: types.CallbackQuery):
        players = load_players()

        user = call.from_user.full_name

        if user not in players:
            players.append(user)
            save_players(players)

        await call.answer("Ты записан ⚽")


    @dp.callback_query(F.data == "football_leave")
    async def leave(call: types.CallbackQuery):
        players = load_players()

        user = call.from_user.full_name

        if user in players:
            players.remove(user)
            save_players(players)

        await call.answer("Убрал из списка ❌")