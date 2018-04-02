from wand.image import Image
from project.settings import SQUEEZE_RATE, SQUEEZE_STEP


async def compress(blob):
    with Image(blob=blob) as image:
        width = int(image.width * SQUEEZE_RATE)
        height = int(image.height * SQUEEZE_RATE)
        image.liquid_rescale(width=width, height=height, delta_x=SQUEEZE_STEP)
        return image.make_blob('jpeg')
