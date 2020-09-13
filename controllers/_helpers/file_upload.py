from werkzeug.utils import secure_filename
import aiofiles, os

async def write_file(path, body):
    async with aiofiles.open(path, 'wb') as f:
        await f.write(body)

def valid_file_size(file_body):
    if len(file_body) < 10485760:
        return True
    return False

async def process_upload(app, data, filename):
    # Create upload folder if doesn't exist
    if not os.path.exists(app.config.UPLOAD_DIR):
        os.makedirs(app.config.UPLOAD_DIR)

    # Clean up the filename in case it creates security risks
    filename = secure_filename(filename)

    file_path = f"{app.config.UPLOAD_DIR}/{filename}"
    await write_file(file_path, data)
    return file_path
