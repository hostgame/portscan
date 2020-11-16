import asyncio
import socket

from aiohttp import web

from middleware import json_error_middleware
from scanner import scan, check_port
from logger import app_logger as logger

routes = web.RouteTableDef()
loop = asyncio.get_event_loop()

@routes.get('/{ip}/{begin_port}/{end_port}')
async def handle(request):
    ip = request.match_info.get('ip')
    begin_port = int(request.match_info.get('begin_port', 0))
    end_port = int(request.match_info.get('end_port', 0))

    # validate ip
    try:
        socket.inet_aton(ip)
    except socket.error:
        raise web.HTTPBadRequest(text='Invalid IP')

    # validate ports
    if not (1 <= begin_port <= 65535):
        raise web.HTTPBadRequest(text='Invalid begin port')
    if not (1 <= end_port <= 65535):
        raise web.HTTPBadRequest(text='Invalid end port')

    report = await scan(ip, begin_port, end_port+1, loop)
    return web.json_response(report)

app = web.Application(middlewares=[json_error_middleware], logger=logger)
app.add_routes(routes)

if __name__ == '__main__':    
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, port=8080)    
    loop.run_until_complete(site.start())
    
    logger.info('Start portscan server on 8080')
    loop.run_forever()