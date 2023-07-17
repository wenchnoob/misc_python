"""
As the number of darts used increases, the accuracy of this simulation increases.
As can be seen by the below table, as the number of darts used increases the mean value gets closer to pi
and the standard deviation gets smaller.

# of darts
10:         3.251999999999999 ± 0.4203199999999998
100:        3.149200000000001 ± 0.133632
1000:       3.138600000000002 ± 0.041612000000000066
10000:      3.141784 ± 0.012827680000000003
100000:     3.1412112000000008 ± 0.004291999999999994
10000000:   3.1414904760000013 ± 0.00042530000000000177
"""

from math import hypot
from random import uniform


def pi_mont_carlo(maxdarts):
    c = 0
    for _ in range(maxdarts):
        x = uniform(0, 1)
        y = uniform(0, 1)

        if hypot(x, y) <= 1:
            c += 1

    return (c / maxdarts) * 4


# print(pi_mont_carlo(100000))


def avg(ls):
    return sum(ls) / len(ls)


def std_dev(ls):
    average = avg(ls)
    n_ls = [abs(x - average) for x in ls]
    return sum(n_ls) / len(n_ls)


t_cases = [10000000]  # [10, 100, 1000, 10000, 100000, 1000000]
for case in t_cases:
    ls = []
    for _ in range(100):
        v = pi_mont_carlo(case)
        ls.append(v)
        print(f'{_}: {v}')
    print(f'{case}: {avg(ls)} ± {std_dev(ls)}')
