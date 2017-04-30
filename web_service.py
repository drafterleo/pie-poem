from aiohttp import web
import aiohttp_cors  # https://github.com/aio-libs/aiohttp-cors
import os
import sys
import json

import semantics as sem
import make_poems_model as mpm
import analyze_poem as ap

from typing import Callable

# curl -X POST -d "words=%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81" localhost:8081/poems
# curl -X POST --data-urlencode "words=запрос" localhost:8081

w2v_model = None
poems_model = None


def load_models():
    global w2v_model, poems_model
    if sys.platform.startswith("win"):
        w2v_model = sem.load_w2v_model("c:/data/ruscorpora.model.bin.gz")
    else:
        w2v_model = sem.load_w2v_model("/data/ruscorpora.model.bin.gz")
    poems_model = mpm.load_poems_model("poems_model_big.dat", w2v_model, vectorize=True)


def setup_routes(app: web.Application):
    # Configure default CORS (Cross-Origin Resource Sharing) settings.
    cors = aiohttp_cors.setup(app, defaults={
        "http://127.0.0.1": aiohttp_cors.ResourceOptions(
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


async def index(request: web.Request) -> web.FileResponse:
    return web.FileResponse('./static/index.html')


async def poems(request: web.Request) -> web.Response:
    data = await request.json()
    words = data.get('words', '')
    print('words: ', words)
    if len(words) > 0:
        sim_poems_dict = ap.similar_poems(words[:50], poems_model, w2v_model, topn=10, use_associations=False)  # <- [(p, s) ...]
        sim_poems = [spoem[0].replace('\n', '<br>') for spoem in sim_poems_dict]
        print(sim_poems)
        poems_json = json.dumps(sim_poems, separators=(',', ':'), ensure_ascii=False)
        return web.Response(text=poems_json)
    else:
        return web.Response(text=json.dumps('[]'))


async def error_middleware(app: web.Application, handler: Callable) -> Callable:
    async def middleware_handler(request: web.Request):
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
    app = web.Application(middlewares=[error_middleware])
    load_models()
    setup_routes(app)
    setup_static(app)
    web.run_app(app, host='0.0.0.0', port=8081)


if __name__ == "__main__":
    start_web_server()



