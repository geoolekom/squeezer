import asyncio
import logging
from aiohttp import web

from handlers.get import get
from project.settings import HOST, PORT

logger = logging.getLogger(__name__)

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_get('/', get)
    return app

loop = asyncio.get_event_loop()

try:
    app = loop.run_until_complete(init(loop))
    web.run_app(app=app, host=HOST, port=PORT)
except Exception as e:
    logger.error(e, exc_info=True)
finally:
    loop.close()
