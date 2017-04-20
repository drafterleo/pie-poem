from aiohttp import web
import os
import json

import semantics as sem
import make_poems_model as mpm
import analyze_poem as ap

# curl -X POST -d "words=%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81" localhost:8081/poems
# curl -X POST --data-urlencode "words=запрос" localhost:8081

class PoemsWebServer:

    def __init__(self):

        # init web app
        self.host = '127.0.0.1'
        self.port = 8081
        self.app = web.Application()
        self.setup_static()
        self.setup_routes()

        # load models
        self.w2v = sem.load_w2v_model("c:/data/ruscorpora.model.bin.gz")
        self.pm = mpm.load_poems_model("poems_model_big.dat", self.w2v, vectorize=True)

    def setup_routes(self):
        self.app.router.add_route('GET', '/', self.index)
        self.app.router.add_route('POST', '/poems', self.poems)

    def setup_static(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/static/'
        # print(__file__, path)
        self.app.router.add_static('/css', path + 'css')

    def start_web_server(self):
        web.run_app(self.app, host=self.host, port=self.port)

    # routed methods

    async def index(self, request):
        print(request)
        return web.FileResponse('./static/index.html')

    async def poems(self, request):
        print(request)
        data = await request.post()  # <- {name: val, ...}
        words = data.get('words', '')
        if len(words) > 0:
            print(words)
            sim_poems = ap.similar_poems(words, self.pm, self.w2v, topn=5, use_associations=False)  # <- [(p, s) ...]
            poems = [spoem[0].replace('\n', '<br>') for spoem in sim_poems]
            print(poems)
            poems_json = json.dumps(poems, separators=(',', ':'), ensure_ascii=False)
            return web.Response(text=poems_json)
        else:
            return web.Response(text='[]')


if __name__ == "__main__":
    web_server = PoemsWebServer()
    web_server.start_web_server()



