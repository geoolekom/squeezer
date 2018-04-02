from wand.image import Image


async def compress(blob):
    with Image(blob=blob) as image:
        image.liquid_rescale(width=image.width // 2, height=image.height // 2)
        return image.make_blob('jpeg')
