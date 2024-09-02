from tasks.project import start_tasks
from loguru import logger
import asyncio


async def main():
    logger.info('START SCRIPT')
    await start_tasks()

if __name__ == '__main__':
    asyncio.run(main())
