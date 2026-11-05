import time
import random
def RandPermutation(l: int,r: int,n: int, seed: int):
    random.seed(seed)
    if (r - l + 1) < n:
        return False
    s = set()
    li = []
    while len(li) < n:
        ra = random.randint(l , r)
        if not ra in s:
            s.add(ra)
            li.append(ra)

    random.seed(time.time_ns())
    return li.copy()



if __name__ == "__main__":
    print(RandPermutation(0, 9, 10, 10))
    print(RandPermutation(0, 9, 10, 10))
    print(RandPermutation(0, 9, 10, 10))
    print(RandPermutation(0, 9, 10, 10))
    print(RandPermutation(0, 9, 10, 11))