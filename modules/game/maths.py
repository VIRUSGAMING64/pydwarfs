def p2dist(x1,y1, x2,y2):
    return abs(y2 - y1) + abs(x2 - x1)


def parsedirection(x1,x2):
    if x1 == x2:
        return 0
    if x1 < x2:
        return 1
    return -1