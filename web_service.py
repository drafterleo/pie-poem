from aiohttp import web
import aiohttp_cors  # https://github.com/aio-libs/aiohttp-cors
import os
import sys
import json
# import mkl

from poems_model import PoemsModel

from typing import Callable

# curl -X POST -H "Content-Type: application/json" -d "{ \"words\": \"запрос\" }" 87.117.9.189:8085/poems

pie_model = PoemsModel()


def load_models():
    data_path = "/data/"
    if sys.platform.startswith("win"):
        data_path = "c:/data/"
    pie_model.load_w2v_model(data_path + "ruscorpora_1_300_10.bin.gz")
    # pie_model.load_w2v_model(data_path + "ruwikiruscorpora_0_300_20.bin.gz")
    pie_model.read("./data/poems_model_big.pickle")


def setup_routes(app: web.Application):
    # Configure default CORS (Cross-Origin Resource Sharing) settings.
    cors = aiohttp_cors.setup(app, defaults={
        "localhost": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    app.router.add_route('GET', '/', index)
    cors.add(app.router.add_route('POST', '/poems', poems))


def setup_static(app: web.Application):
    path = os.path.dirname(os.path.realpath(__file__)) + '/static/'
    # print(__file__, path)
    app.router.add_static('/dist', path + 'dist')
    app.router.add_static('/css', path + 'css')


async def index(request: web.Request) -> web.StreamResponse:
    return web.FileResponse('./static/index.html')


async def poems(request: web.Request) -> web.StreamResponse:
    data = await request.json()
    words = data.get('words', '')
    print('words: ', words)
    if len(words) > 0:
        sim_poems_dict = pie_model.similar_poems(words[:50], topn=10)  # <- [(p, s) ...]
        sim_poems = [spoem[0].replace('\n', '<br>') for spoem in sim_poems_dict]
        print(sim_poems)
        poems_json = json.dumps(sim_poems, separators=(',', ':'), ensure_ascii=False)
        return web.Response(text=poems_json)
    else:
        return web.Response(text=json.dumps('[]'))


async def error_middleware(app: web.Application, handler: Callable) -> Callable:
    async def middleware_handler(request: web.Request) -> web.StreamResponse:
        try:
            response = await handler(request=request)
            if response.status == 404:
                return web.FileResponse('./static/404.html')
            return response
        except web.HTTPException as ex:
            if ex.status == 404:
                return web.FileResponse('./static/404.html')
            raise
    return middleware_handler


def start_web_server():
    # print('max threads:', mkl.get_max_threads())
    # print('CPU frequency: ', mkl.get_cpu_frequency())
    app = web.Application(middlewares=[error_middleware])
    load_models()
    setup_routes(app)
    setup_static(app)
    web.run_app(app, host='0.0.0.0', port=8085)


if __name__ == "__main__":
    start_web_server()



