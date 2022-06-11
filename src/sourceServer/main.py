import os
import time
import random
import string

from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse

app = FastAPI()


def random_code(length):
    pool = string.digits + string.ascii_letters
    code = ''
    for i in range(length):
        code += random.choice(pool)
    return code


@app.head('/images', response_class=FileResponse)
async def images_get(path: str):
    return FileResponse(path, filename=path.split('/')[-1])


@app.get('/images', response_class=FileResponse)
async def images_get(path: str):
    return FileResponse(path, filename=path.split('/')[-1])


@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    date = time.strftime('%Y%m%d%H', time.localtime())
    filename = f'{int(time.time())}{random_code(10)}.png'
    pathname = f'temp/{date}'

    if not os.path.exists(pathname):
        os.makedirs(pathname)

    path = f'{pathname}/{filename}'

    with open(path, mode='wb') as f:
        f.write(await file.read())

    return path
