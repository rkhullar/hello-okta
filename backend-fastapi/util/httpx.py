import asyncio

import httpx


async def async_httpx(method: str, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        fn = getattr(client, method)
        return await fn(*args, **kwargs)


def wrapped_async_httpx(method: str, *args, **kwargs):
    # TODO: this probably isn't needed
    event_loop = asyncio.get_event_loop()
    future = async_httpx(method, *args, **kwargs)
    return event_loop.run_until_complete(future)


if __name__ == '__main__':
    # TODO: move to unit / integration tests
    test_url = 'http://petstore-demo-endpoint.execute-api.com/petstore/pets'

    async def test_async():
        response = await async_httpx(method='get', url=test_url)
        print(response.json())

    asyncio.run(test_async())
