import sys
import tornado.web
from tornado import web
import pandas as pd
import logging.config

logging.config.fileConfig('resources/logging.ini')
logger = logging.getLogger(__file__)


def read_nutrition_data(data_path):
    df = pd.read_excel(data_path)
    return df


class StaticGlobalObjects:

    TEMPLATE_DIRECTORY = "templates/"
    PUBLIC_ROOT = "resources/web"
    NUTRITION_DATA_PATH = "resources/data/nutritions.xlsx"
    NUTRITION_DATA = read_nutrition_data(NUTRITION_DATA_PATH)

    def __init__(self):
        pass


class MainHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("templates/home.html",
                    breakfast_selections="")


class BreakfastHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        selections = []
        for arg in self.request.arguments:
            arg_count = int(round(float(self.get_argument(arg))))
            if arg_count > 0:
                candidates = StaticGlobalObjects.NUTRITION_DATA.loc[StaticGlobalObjects.NUTRITION_DATA['Grup'] == arg]
                df = candidates.sample(arg_count)
                if df.shape[0] > 0:
                    selections.append(df)
        if len(selections) > 0:
            self.render("templates/home.html",
                        breakfast_selections=pd.concat(selections)
                        .to_html(classes=["table-bordered", "table-striped", "table-hover"]))


def make_app():
    settings = dict(
        debug=True,
        static_path=StaticGlobalObjects.PUBLIC_ROOT,
        template_path=StaticGlobalObjects.PUBLIC_ROOT
    )
    handlers = [
        (r"/", MainHandler),
        (r"/home", MainHandler),
        (r"/kahvalti", BreakfastHandler),
        (r'/(.*)', web.StaticFileHandler, {'path': StaticGlobalObjects.PUBLIC_ROOT}),
    ]
    return web.Application(handlers, **settings)


if __name__ == "__main__":
    app = make_app()
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = "8081"
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()