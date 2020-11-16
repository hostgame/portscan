from aiohttp import web

from logger import app_logger as logger

@web.middleware
async def json_error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        logger.error(ex.text)
        return web.json_response({'error': ex.text}, status=ex.status)