import tornado.web
import tornado.escape
from db.model import Card, CardType
from handler.v1.base import APIHandler


class CardTypeHandler(APIHandler):
    async def _get(self):
        id = self.get_argument("id", None)
        tp = self.get_argument("tp", None)
        name = self.get_argument("name", None)
        page = int(self.get_argument("page", "1"))
        size = int(self.get_argument("size", "10"))
        card_type = CardType(name=name, id=id, tp=tp)
        types, count = card_type.query(page=page, size=size)
        return self.send_json({'cards': types, 'count': count})

    async def _post(self):
        data = tornado.escape.json_decode(self.request.body)
        card_type = CardType(**data)
        card_type.add()
        return self.send_json()

    async def _delete(self):
        id = self.get_argument("id")
        card_type = CardType(id=id)
        card_type.delete()
        return self.send_json()

    async def _put(self):
        data = tornado.escape.json_decode(self.request.body)
        card_type = CardType(**data)
        card_type.update()
        return self.send_json()
