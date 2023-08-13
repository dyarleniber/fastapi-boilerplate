import logging

from .types import Config


class Logger:
    def __init__(self, config: Config):
        self.config = config
        logging.basicConfig(
            filename="log.log",
            encoding="utf-8",
            level=self.config.log_level,
            format="%(asctime)s :: %(levelname)-8s :: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S %Z",
        )

    def debug(self, message: str):
        logging.debug(message)

    def info(self, message: str):
        logging.info(message)

    def warning(self, message: str):
        logging.warning(message)

    def error(self, message: str):
        logging.error(message)

    def critical(self, message: str):
        logging.critical(message)
