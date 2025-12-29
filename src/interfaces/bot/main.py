from aiogram import Dispatcher

from src.infrastructure.database.session import engine

from src.common.logging.logger_main import logger

from .bot_init import bot
from . import handle_router


async def on_shutdown() -> None:
    """Clean up resources on shutdown"""
    try:
        await bot.session.close()
        await engine.dispose()
        logger.info("All resources cleaned up")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    

async def on_startup() -> None:
    """Initialize bot, start services"""
    logger.info("🚀Starting bot services...")

    dp = Dispatcher()
    
    dp.include_router(handle_router.router)
    try:
        logger.info("✅ Bot started succesfully!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Startup error: {e}")
        return None
    finally:
        await on_shutdown()
    

if __name__ == '__main__':
    from asyncio import run
    
    try:
        run(on_startup())
    except KeyboardInterrupt:
        logger.info("⚠️ Bot stopped manually.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")