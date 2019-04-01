import tornado.ioloop
from tornado import web
from tornado.escape import json_decode
import dbtest

class MH(web.RequestHandler):
    def post(self):
        job = json_decode(self.request.body)
        if type(job)==dict:
            job = list(job.values())[0]
        id = dbtest.addline(job)
        self.write({"result": "OK", "id": id})

    def get(self):
        job = json_decode(self.request.arguments['id'][0])
        p = dbtest.readlinesyield()
        pie=False
        for i in p:
            if i[0] == job:
                self.write({"id": i[0], "date": str(i[1]), "raw": i[2], "sorted":i[3]})
                pie = True
        if pie==False:
            self.write({"result": "Error"})

if __name__ == "__main__":
    app = web.Application([(r"/", MH)])
    app.listen(4444)
    tornado.ioloop.IOLoop.instance().start()