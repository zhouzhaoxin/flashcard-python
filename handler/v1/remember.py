import tornado

from config import REMEMBER
from db.db import generate_unknown_ids, remember_next, get_cards_by_ids
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

    async def refresh(self):
        uid = self.get_argument("uid")
        tp = self.get_argument("tp")
        generate_unknown_ids(uid, tp)
        return self.send_json()

    async def index(self):
        uid = self.get_argument("uid")
        tp = self.get_argument("tp")
        curr = int(self.get_argument("curr"))
        if uid not in REMEMBER:
            generate_unknown_ids(uid, tp)
        print(REMEMBER)
        ids = REMEMBER[uid]["ids"][(curr - 1) * 10:(curr - 1) * 10 + 10]
        print(ids)
        cards = get_cards_by_ids(ids)
        return self.send_json({
            "cards": cards,
            "c": len(REMEMBER[uid]['ids'])
        })

    async def known(self):
        uid = self.get_argument("uid")
        id = self.get_argument("id")
        tp = self.get_argument("tp")
        card = Card(id=id, known=1)
        card.update()
        generate_unknown_ids(uid, tp)
        return self.send_json()
