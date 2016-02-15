__author__ = 'multiangle'
#========================================================#
#----------------import package--------------------------#
# import python package                                  #
# import from outer package                              #
import tornado.web                                      #
import tornado.ioloop                                   #
import tornado.options                                  #
from tornado.options import define,options             #
# import from this folder                                #
#========================================================#
define('port',default=7000,help='run on the given port',type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',showPage)
        ]
        settings=dict(
            debug=True
        )
        tornado.web.Application.__init__(self,handlers,**settings)

class showPage(tornado.web.RequestHandler):
    def get(self):
        self.write('a;sjdflk')
        self.finish()


if __name__=='__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()