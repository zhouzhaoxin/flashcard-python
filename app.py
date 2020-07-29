import tornado.ioloop
import tornado.web

from handler.v1.card_type import CardTypeHandler
from handler.v1.cards import CardsHandler
from handler.v1.remember import RememberHandler
from handler.v1.users import UsersHandler

ROUTERS = [
    (r"/v1/cards", CardsHandler),
    (r"/v1/users", UsersHandler),
    (r"/v1/card/type", CardTypeHandler),
    (r"/v1/remember/?(index|next|prev|known|login|signup)?", RememberHandler),
]


def make_app():
    return tornado.web.Application(ROUTERS)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
