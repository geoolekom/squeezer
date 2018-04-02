import io

import logging

from project.loop import loop
from project.settings import TELEGRAM_BOT_TOKEN
from aiohttp import web, ClientSession

from squeeze.squeeze import compress

logger = logging.getLogger(__name__)


async def load_file(path):
    url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{path}'
    async with ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            try:
                return await response.read()
            except Exception as e:
                logger.error(e, exc_info=True)
                return b''


async def api_request(method, **data):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}'
    async with ClientSession(loop=loop) as session:
        async with session.post(url, data=data) as response:
            try:
                data = await response.json()
                return data
            except Exception as e:
                logger.error(e, exc_info=True)
                return {}


async def handler(request):
    data = await request.json()
    message = data['message']
    chat_id = message['chat']['id']
    if 'photo' in message:
        photo_sizes = message['photo']
        photo_sizes = [size for size in photo_sizes if size.get('file_size') < 20 * 1024 * 1024]
        photo = photo_sizes[-1]
        file_data = await api_request('getFile', file_id=f'{photo.get("file_id")}')
        data = await load_file(file_data['result']['file_path'])
        processed_data = await compress(data)
        response = {
            'chat_id': f'{chat_id}',
            'photo': io.BytesIO(processed_data)
        }
        await api_request('sendPhoto', **response)
    else:
        response = {
            'chat_id': f'{chat_id}',
            'text': 'Сжимать умею только фотки!'
        }
        await api_request('sendMessage', **response)
    return web.Response(status=200)
