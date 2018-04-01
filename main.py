import logging
from aiohttp import web

from project.loop import loop
from handlers.telegram import handler as tg_handler
from project.settings import HOST, PORT

logger = logging.getLogger(__name__)

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_post('/api/telegram/', tg_handler)
    return app

try:
    app = loop.run_until_complete(init(loop))
    web.run_app(app=app, host=HOST, port=PORT)
except Exception as e:
    logger.error(e, exc_info=True)
finally:
    loop.close()
