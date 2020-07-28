from db.db import generate_unknown_ids, remember_next, remember_prev
from db.model import Card
from handler.v1.base import MobileHandler


class RememberHandler(MobileHandler):
    async def index(self):
        uid = self.get_argument("uid")
        tp = self.get_argument("tp")
        generate_unknown_ids(uid, tp)
        next_id = remember_next(uid)
        return self.send_json(next_id)

    async def next(self):
        uid = self.get_argument("uid")
        return self.send_json(remember_next(uid))

    async def prev(self):
        uid = self.get_argument("uid")
        return self.send_json(remember_prev(uid))

    async def known(self):
        uid = self.get_argument("uid")
        id = self.get_argument("id")
        tp = self.get_argument("tp")
        card = Card(id=id, known=1)
        card.update()
        generate_unknown_ids(uid, tp)
        next_id = remember_next(uid)
        return self.send_json(next_id)
