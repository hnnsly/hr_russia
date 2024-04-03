import asyncio
import logging
import sys
import storage

from bot.bot import router, bot


async def main():
    await router.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
