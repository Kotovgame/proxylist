from .config import URL_FOR_VERIFICATION_PROXY as test_url
from aiohttp import ClientSession
from time import time
from logging import getLogger
from asyncio import create_task, gather, Task
from aiofile import AIOFile, LineReader, Writer
from re import findall


logger = getLogger(__name__)


async def check_proxy(session: ClientSession, proxy: str):
    try:
        start_time = time()
        async with session.get(test_url, proxy=proxy) as response:
            return (proxy, response.status == 200, time() - start_time, "")
    except Exception as error:
        return (proxy, False, -1, error)


async def load_host_port(session: ClientSession, url: str) -> tuple[list[str], int]:
    pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}\b"
    async with session.get(url) as response:
        tasks = findall(pattern, await response.text())
    return tasks, len(tasks)


async def verification_proxy(tasks, size: int | None = None) -> list:
    start_time = time()
    if not size is None:
        logger.info(f"Бот начал опрашивать все прокси сервера {size}")
    tasks = [task for task in await gather(*tasks) if task[1]]
    d_time = time() - start_time
    if not size is None:
        logger.info(f"Удачных ответов: {len(tasks)}/{size} за {(d_time):.0f} секунд")
    return tasks


def create_proxy_task(session: ClientSession, proxies: list[str]) -> list[Task]:
    tasks = [f"http://{proxy}" for proxy in proxies]
    tasks = [check_proxy(session, task) for task in tasks]
    tasks = [create_task(task) for task in tasks]
    return tasks


async def main():
    async with ClientSession() as session:
        async with AIOFile("app/assets/input_http_proxy.txt", "r+") as rfile:
            async for url in LineReader(rfile):
                proxies, size = await load_host_port(session, url)
                tasks = create_proxy_task(session, proxies)
                tasks = await verification_proxy(tasks, size)
                path = f"app/assets/output/{time()}-{size}.txt"
                async with AIOFile(path, "w+") as wfile:
                    writer = Writer(wfile)
                    for proxy, _, delay, _ in tasks:
                        await writer(f"{proxy} {delay:.3f}\n")
