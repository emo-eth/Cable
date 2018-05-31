def map_dict(value, keys):
    out = dict()
    for key in keys:
        out[key] = value
    return out


def stargs(f):
    def helper(args):
        return f(*args)
    return helper


def merge_dicts(a, b):
    a.update(b)
    return a


def min_max(coll):
    if not coll:
        return None
    mn = float('inf')
    mx = float('-inf')
    for e in coll:
        if e < mn:
            mn = e
        if e > mx:
            mx = e
    return mn, mx
