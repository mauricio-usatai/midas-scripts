import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger()


def log_execution(func):
    def wrapper(container_name: str, *args, **kwargs):
        logger.info("Starting %s", container_name)
        result = func(container_name, *args, **kwargs)
        logger.info("%s done", container_name)
        return result

    return wrapper
