from aiohttp import web
import os

import semantics as sem
import make_poems_model as mpm

async def index(request):
    print(request)
    return web.FileResponse('./static/index.html')


async def poems(request):
    print(request)
    data = await request.post()
    print(data['words'])
    return web.Response(text=data['words'])


def setup_routes(app):
    app.router.add_route('GET', '/', index)
    app.router.add_route('POST', '/poems', poems)


def setup_static(app):
    path = os.path.dirname(os.path.realpath(__file__)) + '/static/'
    print(__file__, path)
    app.router.add_static('/css', path + 'css')


def load_models():
    w2v = sem.load_w2v_model("c:/data/ruscorpora.model.bin.gz")
    pm = mpm.load_poems_model("poems_model.dat", w2v, vectorize=True)


# curl -X POST -d "words=%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81" localhost:8081/poems
# curl -X POST --data-urlencode "words=запрос" localhost:8081
def start_web_server():
    # load_models()
    app = web.Application()
    setup_static(app)
    setup_routes(app)
    web.run_app(app, host='127.0.0.1', port=8081)


start_web_server()



