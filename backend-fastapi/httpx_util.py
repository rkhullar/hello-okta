import asyncio

import httpx


async def async_httpx_get(*args, **kwargs):
    async with httpx.AsyncClient() as client:
        return await client.get(*args, **kwargs)


def wrapped_async_httpx_get(*args, **kwargs):
    event_loop = asyncio.get_event_loop()
    future = async_httpx_get(*args, **kwargs)
    return event_loop.run_until_complete(future)
