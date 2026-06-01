import os
from aiogram import Bot, Dispatcher
from aiohttp import web

from football_manager import register_handlers

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# подключаем футбольную логику
register_handlers(dp)


app = web.Application()


async def handler(request):
    from aiogram import types

    update = types.Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return web.Response(text="ok")


app.router.add_post("/", handler)


if __name__ == "__main__":
    web.run_app(app, port=8080)