


def OnlyBitmask(tp: int, allows:list[int]):
    for bit in allows:
        if tp&bit:
            tp^=bit
            
    if tp == 0:
        return True
    return False