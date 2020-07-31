import random

from db.base import session, BaseMixin
from db.model import Card
from config import REMEMBER


def generate_unknown_ids(uid, tp):
    card = Card(uid=uid, known=1, tp=tp)
    cards, _ = card.query()
    ids = [card['id'] for card in cards]
    random.shuffle(ids)
    remember_dict = {
        'ids': ids,
    }
    REMEMBER[uid] = remember_dict


def remember_next(uid, curr):
    ids = REMEMBER[uid]['ids']
    return ids[curr % len(ids)]


def get_cards_by_ids(ids):
    cards = session.query(Card).filter(Card.id.in_(ids)).all()
    return [BaseMixin.model2dict(r) for r in cards]
