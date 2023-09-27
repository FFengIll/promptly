import asyncio
import time

import pytest


async def sleep(i):
    print("hello")
    time.sleep(1)
    print("bye")
    return i


@pytest.mark.asyncio
async def test_await_in_loop():
    res = []
    for i in range(5):
        item = sleep(i)
        print(item)
        res.append(item)
    g = asyncio.gather(*res)
    res = await g
    print(res)
    return res
