import random

from db.model import Card
from config import REMEMBER


def generate_unknown_ids(uid, tp):
    card = Card(uid=uid, known=0, tp=tp)
    cards, _ = card.query()
    ids = [card['id'] for card in cards]
    random.shuffle(ids)
    remember_dict = {
        'ids': ids,
        'curr': -1,
    }
    REMEMBER[uid] = remember_dict


def remember_next(uid):
    ids = REMEMBER[uid]['ids']
    REMEMBER[uid]['curr'] += 1
    return ids[REMEMBER[uid]['curr'] % len(ids)]


def remember_prev(uid):
    ids = REMEMBER[uid]['ids']
    REMEMBER[uid]['curr'] -= 1
    return ids[REMEMBER[uid]['curr'] % len(ids)]
