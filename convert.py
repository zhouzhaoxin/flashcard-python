from typing import List, Dict

demo_list = [
    {'pid': 'a', 'name': 'b'},
    {'name': 'a'},
    {'pid': 'a', 'name': 'c'},
    {'pid': 'a', 'name': 'd'},
    {'name': 'e'},
    {'pid': 'e', 'name': 'f'},
    {'pid': 'f', 'name': 'g'},
]

demo_res = {
    'a': {
        'b': {},
        'c': {},
        'd': {},
    },
    'e': {
        'f': {
            'g': {}
        }
    }
}


def find_parent(parent: Dict, name: str, star: List) -> None:
    """
    use {parent} build parent chain {star} start at {name}
    """
    pid = parent[name]
    while pid:
        star.append(pid)
        pid = parent[pid]


def build_res(res: Dict, star: List) -> None:
    """
    use parent chain {star} build result dict {res}
    """
    curr = res
    for i in range(len(star) - 1, -1, -1):
        s = star[i]
        if s not in curr:
            curr.setdefault(s, {})
        curr = curr[s]


def convert_format(datas: List[dict]) -> Dict:
    """
    convert {datas} list to {res} tree dict
    """
    parent = {}
    res = {}
    for data in datas:
        if 'name' not in data:
            raise Exception("argument error")
        name = data['name']
        if 'pid' not in data:
            parent[name] = None
            res.setdefault(name, {})
        else:
            pid = data['pid']
            parent[name] = pid
            if pid not in parent:
                parent[pid] = None
            star = [name]
            find_parent(parent, name, star)
            build_res(res, star)
    return res


print(convert_format(demo_list))
