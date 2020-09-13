import aiofiles

async def save_settings(path, config):
    async with aiofiles.open(path, 'wb') as f:
        config.write(f)
