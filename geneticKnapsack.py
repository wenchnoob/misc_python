from copy import copy
from random import choice, random, randint


class Item:

    def __init__(self, value, weight, name=None):
        self.name = name
        self.value = value
        self.weight = weight

    def __repr__(self):
        return f'Item(Name={self.name}, Value={self.value}, Weight={self.weight})'

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        if self.value == other.value:
            return 0
        return 1

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def get_weight(self):
        return self.weight

    def get_value(self):
        return self.value


class Chromosome:

    __crossover_rate__ = .7
    __mutation_rate__ = .001

    def __init__(self, rep, items, mx_cap):
        self.rep = rep
        self.items = items
        self.mx_cap = mx_cap
        self.weight = None
        self.value = None
        self.calcValWeight()

    def copy(self):
        return copy(self)

    def calcValWeight(self):
        val = 0
        weight = 0
        for idx, bit in enumerate(self.rep):
            if bit == '1':
                item = self.items[idx]
                val += item.value
                weight += item.weight

        if weight > self.mx_cap:
            idx = self.rep.index('1')
            self.rep[idx] = '0'
            self.calcValWeight()
        else:
            self.value = val
            self.weight = weight

    @classmethod
    def rand(cls, items, mx_cap):
        rep = [str(choice([0, 1])) for x in range(len(items))]
        return Chromosome(rep, items, mx_cap)

    def __repr__(self):
        return f'Chromosome(Rep={self.rep}, Value={self.value}, Weight={self.weight})'

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        if self.value == other.value:
            return 0
        return 1

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def get_packed(self):
        return [self.items[i] for i, bit in enumerate(self.rep) if bit == '1']

    def crossover(self, other):
        if not isinstance(other, Chromosome) or \
                random() > Chromosome.__crossover_rate__:
            return None
        
        c_point = randint(0, len(self.rep))
        temp = self.rep[0:c_point] + other.rep[c_point:]
        other.rep = other.rep[0:c_point] + self.rep[c_point:]
        self.rep = temp
        self.calcValWeight()
        other.calcValWeight()

    def point_mutation(self, mutation_rate=.001):
        for i in range(len(self.rep)):
            if random() < mutation_rate:
                self.rep[i] = "1" if self.rep[i] == "0" else "0"
        self.calcValWeight()


stuff = [Item(3, 2, "A"), Item(5, 4, "B"), Item(6, 5, "C"), Item(8, 7, "D"), Item(10, 9, "E")]

population = []
for i in range(10):
    population.append(Chromosome.rand(stuff, 20))

gens = 500
population.sort()
for _ in range(gens):
    new_gen = []
    for i in range(0, len(population) - 1, 2):
        parent_a = population[i]
        parent_b = population[i+1]
        child_a = parent_a.copy()
        child_b = parent_b.copy()
        child_a.crossover(child_b)

        child_a.point_mutation()
        child_b.point_mutation()

        new_gen.append(parent_a)
        new_gen.append(parent_b)
        new_gen.append(child_a)
        new_gen.append(child_b)

    new_gen.sort(reverse=True)
    population = new_gen[:10]

print(population[0])



