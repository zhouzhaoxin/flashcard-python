import tornado.web
import tornado.escape
from db.model import Card
from handler.v1.base import APIHandler


class CardsHandler(APIHandler):
    async def _get(self):
        id = self.get_argument("id", None)
        front = self.get_argument("front", None)
        back = self.get_argument("back", None)
        known = self.get_argument("known", None)
        tp = self.get_argument("tp", None)
        page = int(self.get_argument("page", "1"))
        size = int(self.get_argument("size", "10"))
        card = Card(id=id, front=front, back=back, known=known, tp=tp)
        cards, count = card.query(page=page, size=size)
        return self.send_json({'cards': cards, 'count': count})

    async def _post(self):
        data = tornado.escape.json_decode(self.request.body)
        card = Card(**data)
        card.add()
        return self.send_json()

    async def _delete(self):
        id = self.get_argument("id")
        card = Card(id=id)
        card.delete()
        return self.send_json()

    async def _put(self):
        data = tornado.escape.json_decode(self.request.body)
        card = Card(**data)
        card.update()
        return self.send_json()
