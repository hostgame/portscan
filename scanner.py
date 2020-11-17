import asyncio
from logger import app_logger as logger

async def check_port(ip, port):
    logger.info("Check {} on {}".format(port, ip))
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        return {"port": port, "state": "open"}
    except:
        return {"port": port, "state": "close"}

async def scan(ip, begin, end):
    tasks = [asyncio.ensure_future(check_port(ip, p)) for p in range(begin, end)]
    responses = await asyncio.gather(*tasks)
    return responses

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(scan('127.0.0.1', 8075, 8085))
    loop.run_until_complete(future)
    print(future.result())
