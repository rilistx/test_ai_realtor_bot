import asyncio
import logging
import platform

from core import unpacker


async def main() -> None:


    await unpacker()


if __name__ == "__main__":
    try:
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(
                policy=asyncio.WindowsSelectorEventLoopPolicy(),
            )

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("This bot stopped 😈")
