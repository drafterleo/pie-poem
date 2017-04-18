from aiohttp import web

import semantics as sem
import make_poems_model as mpm

async def index(request):
    print(request)
    return web.FileResponse('./web_client.html')


async def poems(request):
    print(request)
    data = await request.post()
    print(data['words'])
    return web.Response(text=data['words'])


def setup_routes(app):
    app.router.add_route('GET', '/', index)
    app.router.add_route('POST', '/poems', poems)


# w2v = sem.load_w2v_model("c:/data/ruscorpora.model.bin.gz")
# pm = mpm.load_poems_model("poems_model.dat", w2v, vectorize=True)

app = web.Application()
setup_routes(app)
web.run_app(app, host='127.0.0.1', port=8081)

# curl -X localhost:8081
# curl -X POST -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" --data-ascii "words=%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81" localhost:8081
# curl -X POST -d "words=%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81" localhost:8081
# curl -X POST --data-urlencode "words=запрос" localhost:8081


