import asyncio, aiofiles, json
from aiohttp import ClientSession, ClientTimeout, ClientError
from aiohttp.http_exceptions import HttpProcessingError


CONNECTIONS_COUNT = 5
FILE_PATH = './results.jsonl'
URLS = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def write_to_file(url, status):
    async with aiofiles.open(FILE_PATH, 'a') as file:
        await file.write(json.dumps({"url": url, "status_code": status}) + '\n')


async def fetch_url(semaphore: asyncio.Semaphore, client: ClientSession, url: str):
    async with semaphore:
        try:
            async with client.get(url) as response:
                await write_to_file(url, response.status)
        except (ClientError, asyncio.TimeoutError, HttpProcessingError):
            await write_to_file(url, 0)


async def fetch_urls():
    async with ClientSession(timeout=ClientTimeout(5)) as client:
        semaphore = asyncio.Semaphore(CONNECTIONS_COUNT)
        tasks = [fetch_url(semaphore, client, url) for url in URLS]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(fetch_urls())