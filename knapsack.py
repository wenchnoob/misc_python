from random import randint




ls = []
for _ in range(15):
    ls.append(Item(randint(1, 10), randint(5, 16)))
print(ls)


def greedy_knapsack(items, mx_cap):
    items.sort(reverse=True)
    packed = []
    cap = 0
    val = 0
    idx = 0

    while cap < mx_cap and idx < len(items):
        item = items[idx]
        if cap + item.weight <= mx_cap:
            packed.append(item)
            cap += item.weight
            val += item.value
        idx += 1

    return val, packed


v, p = greedy_knapsack(ls, 50)
print(v, p)


def greedy_fractional_knapsack(items, mx_cap):
    items.sort(key=lambda x: x.value / x.weight, reverse=True)
    packed = []
    cap = 0
    val = 0
    idx = 0

    while cap < mx_cap and idx < len(items):
        item = items[idx]
        if cap + item.weight <= mx_cap:
            packed.append(item)
            cap += item.weight
            val += item.value
        else:
            ratio = (mx_cap - cap) / item.weight
            val += item.value * ratio
            cap += item.weight * ratio
            packed.append(Item(ratio * item.value, ratio * item.weight))

        idx += 1

    return val, packed


v, p = greedy_fractional_knapsack(ls, 50)
print(v, sum([x.weight for x in p]), p)


def recursive_knapsack(items, current, mx_cap):
    result = 0

    item = items[0]
    if current < len(items):
        withoutItem = recursive_knapsack(items, current + 1, mx_cap)
        withItem = 0
        if item.weight <= mx_cap:
            withItem += item.value
            withItem += recursive_knapsack(items, current + 1, mx_cap - item.weight)
        result = max(withoutItem, withItem)

    return result


v = recursive_knapsack(ls, 0, 50)
print(v)

import numpy as np
def dp_knapsack(items, mx_cap):
    ROWS = len(items) + 1
    COLS = mx_cap + 1

    partial_solutions = np.zeros([ROWS, COLS], dtype="int32")

    for i in range(1, ROWS):
        for c in range(1, COLS):
            item = items[i - 1]
            bestSoFar = partial_solutions[i-1][c]
            if item.weight <= c:
                withItem = item.value
                capLeft = c - item.weight
                withItem += partial_solutions[i - 1][capLeft]
                if withItem > bestSoFar:
                    bestSoFar = withItem
            partial_solutions[i][c] = bestSoFar

    return partial_solutions[ROWS - 1][COLS - 1], partial_solutions

def makeItemList(solution, items, mx_cap):
    i = len(items)
    k = mx_cap
    packed = []

    while i > 0 and k > 0:
        if solution[i][k] != solution[i-1][k]:
            i -= 1
            packed.append(items[i])
            k -= items[i].weight
        else:
            i -= 1
    return packed

v, solution = dp_knapsack(ls, 50)
packed = makeItemList(solution, ls, 50)
print(v, packed)