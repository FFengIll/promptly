import random
import time


async def test_await_in_loop():
    def sleep():
        time.sleep(5)
        return random.randint(0, 10)

    for i in range(5):
        res = await sleep()
        print(res)
