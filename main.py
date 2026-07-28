import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher

from handlers import get_handlers_router
from config import TOKEN
from middlewares.database import DbSessionMiddleware
from middlewares.user import UserMiddleware
from database.pool import create_pool, close_pool
from database.migrations.runner import run_migrations
from services.scheduler import init_scheduler


async def _healthcheck(request: web.Request) -> web.Response:
    """Отвечает 200 OK. Бот работает через long polling
    и своего HTTP-сервера не имеет, поэтому этот эндпоинт нужен
    исключительно для прохождения проверок платформ."""
    return web.Response(text="ok")


async def start_healthcheck_server() -> None:
    """Поднимает лёгкий aiohttp-сервер на 80 порту параллельно с polling."""
    app = web.Application()
    app.router.add_get("/healthz", _healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 80)
    await site.start()
    logging.info("Healthcheck-сервер запущен на порту 80 (/healthz)")


async def main():
    dp = Dispatcher()
    bot = Bot(token=TOKEN)

    # Создаём пул соединений с PostgreSQL и сразу применяем миграции
    pool = await create_pool()
    await run_migrations(pool)

    dp.include_router(get_handlers_router())

    await init_scheduler(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    # Middleware теперь раздаёт хендлерам asyncpg.Connection из пула,
    # а не открывает aiosqlite.connect на каждый Update
    dp.update.middleware(DbSessionMiddleware(pool=pool))
    dp.update.middleware(UserMiddleware())

    # Открываем 80 порт до входа в цикл polling
    await start_healthcheck_server()

    try:
        # Бесконечный цикл для автоматического переподключения
        while True:
            try:
                logging.info("Запуск поллинга...")
                await dp.start_polling(bot)
            except Exception as e:
                logging.error(f"Сетевая ошибка или сбой: {e}. Перезапуск через 5 секунд...")
                await asyncio.sleep(5)
    finally:
        # Закрываем пул соединений при остановке приложения
        await close_pool(pool)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Bot has been started")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")