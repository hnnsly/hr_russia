import asyncio
import logging
import sys
import storage
from bot import bot, router
from bot import handlers


async def main():
    await router.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
