import logging

def logger() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        filename="console.log",
        filemode="w",
        format="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(lineno)d | %(message)s",
        encoding='utf-8',
    )
