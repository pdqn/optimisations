import json
import time
import uuid

import tornado.ioloop
import tornado.httpserver

from random import randint
from tornado.gen import multi
from tornado import web

PORT = 8889

class MainHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-type', 'application/json')

    def do_processing(self, instance):
        print("Executing {}".format(instance["identifier"]))
        print("Sleeping for {} seconds".format(instance["sleep_time"]))
        time.sleep(instance["sleep_time"])
        print("Finished Executing {}".format(instance["identifier"]))
        return instance

    async def get(self):
        items = []
        for _ in range(10):
            items.append({
                "identifier": str(uuid.uuid4()),
                "sleep_time": randint(1, 10)
            })
        
        responses =  multi([
            tornado.ioloop.IOLoop.current().run_in_executor(None, self.do_processing, item) for item in items
        ])

        #responses = [self.do_processing(item) for item in items]

        return self.write(json.dumps({
            "success": True,
            "data": responses,
            "message": "PONG"
        }))


def make_app():
    settings = {
        "debug": False
    }
    return web.Application([
        ("/ping", MainHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    if True:
        app.listen(PORT)
        print(":: Starting development server on http://0.0.0.0:{}".format(PORT))
    else:
        server = tornado.httpserver.HTTPServer(app)
        server.bind(PORT)
        print(":: Starting production server on http://0.0.0.0:{}".format(PORT))
        server.start(0)  # forks one process per cpu
    tornado.ioloop.IOLoop.current().start()