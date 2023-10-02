from app.config import LOGGER_FORMAT
from logging import basicConfig, INFO
from app.main import main, logger
import asyncio


if __name__ == "__main__":
    try:
        basicConfig(level=INFO, format=LOGGER_FORMAT)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, StopIteration, SystemExit):
        logger.info("Работа завершена!")
