def Initialize(gametype, buff):
    buff = buff.decode()
    lines = buff.split("\n")
    for line in lines:
        line = line.split(' ')
        if len(line) != 2:
            return False
        attr = line[0]
        val = line[1]
        if not hasattr(gametype, attr):
            return False

        setattr(gametype, attr, val)

    return True
