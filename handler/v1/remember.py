import tornado

from db.db import generate_unknown_ids, remember_next, remember_prev
from db.model import Card, User
from handler.v1.base import MobileHandler


class RememberHandler(MobileHandler):

    async def _login(self):
        data = tornado.escape.json_decode(self.request.body)
        user = User(**data)
        user, c = user.explict_query()
        assert c == 1, "用户名或密码错误"
        return self.send_json(user[0])

    async def _signup(self):
        data = tornado.escape.json_decode(self.request.body)
        user = User(username=data['username'])
        _, c = user.explict_query()
        assert c == 0, "用户已存在"
        user = User(**data)
        user.add()
        return self.send_json(user.model2dict(user))

    async def index(self):
        uid = self.get_argument("uid")
        tp = self.get_argument("tp")
        generate_unknown_ids(uid, tp)
        next_id = remember_next(uid)
        card = Card(id=next_id)
        cards, _ = card.query()
        return self.send_json(cards[0])

    async def next(self):
        uid = self.get_argument("uid")
        card = Card(id=remember_next(uid))
        cards, _ = card.query()
        return self.send_json(cards[0])

    async def prev(self):
        uid = self.get_argument("uid")
        card = Card(id=remember_prev(uid))
        cards, _ = card.query()
        return self.send_json(cards[0])

    async def known(self):
        uid = self.get_argument("uid")
        id = self.get_argument("id")
        tp = self.get_argument("tp")
        card = Card(id=id, known=1)
        card.update()
        generate_unknown_ids(uid, tp)
        next_id = remember_next(uid)
        return self.send_json(next_id)
