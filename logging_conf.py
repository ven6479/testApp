from loguru import logger


class LoggerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.initialize_logger()
        return cls._instance

    def initialize_logger(self):
        log_settings = {
            "debug": {
                "level": "DEBUG",
                "path": "./logs/debug/{time}.log"
            },
            "info": {
                "level": "INFO",
                "path": "./logs/info/{time}.log"
            },
            "warning": {
                "level": "WARNING",
                "path": "./logs/warning/{time}.log"
            }
        }

        for key, value in log_settings.items():
            self.configure_logger(level=value["level"], log_filepath=value["path"])

    def configure_logger(self, level, log_filepath):
        logger.add(log_filepath,
                   level=level,
                   enqueue=True,
                   rotation="10 MB",
                   compression="zip",
                   format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{file}</cyan> : <cyan>{line}</cyan> | <level>{message}</level>",
                   serialize=True)

# Usage:
