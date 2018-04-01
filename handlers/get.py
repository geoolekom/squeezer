import json
from aiohttp import web


async def get(request):
    return web.Response(status=200, body=json.dumps({'status': 'OK'}))
