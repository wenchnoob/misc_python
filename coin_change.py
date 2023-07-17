import sys

mapping = [(1, "Brown"),
           (2, "Pink"),
           (5, "Orange"),
           (15, "Pink"),
           (30, "Brown"),
           (100, "Orange"),
           (200, "Octarine")]


mapping.reverse()

def merge(mp1, mp2):
    mp = {}
    for key in mp1:
        if key in mp2:
            mp[key] = mp1[key] + mp2[key]
        else:
            mp[key] = mp1[key]

    for key in mp2:
        if key not in mp1:
            mp[key] = mp2[key]

    return mp
    print(mp)


def solve(value, memo):
    # print(value)
    # print(colors)

    if value < 0:
        return None

    match value:
        case 1:
            return {"Brown": 1, "Pink": 0, "Orange": 0, "Octarine": 0}
        case 2:
            return {"Brown": 0, "Pink": 1, "Orange": 0, "Octarine": 0}
        case 5:
            return {"Brown": 0, "Pink": 0, "Orange": 1, "Octarine": 0}
        case 200:
            return {"Brown": 0, "Pink": 0, "Orange": 0, "Octarine": 1}

    if value in memo:
        print(f'{value} is memoized as {memo[value]}')
        return memo[value]

    diff = sys.maxsize
    res = None
    for e in mapping:
        t = {e[1]: 1}
        r = solve(value - e[0], memo)
        if r is not None:
            d = max(r.values()) - min(r.values())
            # print(r)
            # print(d)
            if d == 0:
                return merge(t, r)
            if d == diff:
                if list(r.values()).count(0) < list(res.values()).count(0):
                    res = merge(t, r)
            if d < diff:
                diff = d
                res = merge(t, r)

    if res is not None:
        memo[value] = res
    return res


value = 10
memo = {}
print(solve(value, memo))

# value = 100
# memo = {}
# print(solve(value, memo))
#
# value = 1000
# memo = {}
# print(solve(value, memo))
#
# value = 1337
# memo = {}
# print(solve(value, memo))
#
# value = 31415
# memo = {}
# print(solve(value, memo))


