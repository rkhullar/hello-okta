import asyncio
import httpx


async def async_get(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.raise_for_status()
    return response.json()


def wrapped_async_get(url: str) -> dict:
    loop = asyncio.get_event_loop()
    future = async_get(url)
    return loop.run_until_complete(future)


if __name__ == '__main__':
    async def test_async():
        test_url = 'http://localhost:8000/hello'
        data = await async_get(test_url)
        print(data)

    def test_wrapped_async():
        test_url = 'http://localhost:8000/hello'
        data = wrapped_async_get(test_url)
        print(data)

    # asyncio.run(test_async())
    test_wrapped_async()
