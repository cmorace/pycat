def flatten(l):
    new_l = []
    for x in l:
        for y in x:
            new_l.append(y)
    return new_l

def any_in(a, b):
    return not set(a).isdisjoint(b)

def all_in(a, b):
    for k in a:
        if k not in b:
            return False
    return True

def x_implies_y(x,y):
    return y if x else True    