import tornado.escape
import tornado.web

from db.model import User
from handler.v1.base import APIHandler


class UsersHandler(APIHandler):
    async def _get(self):
        id = self.get_argument("id", None)
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        page = int(self.get_argument("page", "1"))
        size = int(self.get_argument("size", "10"))
        card = User(id=id, username=username, password=password)
        cards, count = card.query(page=page, size=size)
        return self.send_json({'cards': cards, 'count': count})

    async def _post(self):
        data = tornado.escape.json_decode(self.request.body)
        user = User(**data)
        user.add()
        return self.send_json()

    async def _delete(self):
        id = self.get_argument("id")
        user = User(id=id)
        user.delete()
        return self.send_json()

    async def _put(self):
        data = tornado.escape.json_decode(self.request.body)
        user = User(**data)
        user.update()
        return self.send_json()
