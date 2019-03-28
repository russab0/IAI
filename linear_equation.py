"""Exercise: Solve Linear Equation using GA

-- Compose a simple (2-3 weights) linear equation, e.g. y = w1*x1 + w2*x2
-- Create a test and a validation set. Each of them should have 
set of values of x1, x2, y (for the former example) – an array of examples
-- Code a genetic algorithm that tries to find the best w1, w2 that minimize
the error"""

from random import randint

INF = 10**9
POPULATION_SIZE = 10
EVOLUTION_CYCLE = 10
BEST_PARENTS_COUNT = 3


def fitness(individual):
    assert is_individual(individual)
    x1, x2 = individual
    return - abs(w1 * x1 + w2 * x2 - y)


def sort_by_fitness(arr):
    arr.sort(key = lambda x: fitness(x))
    return arr


def find_maxes(arr, cnt = 1):
    q = sort_by_fitness(arr)
    return q[-cnt:]


def generate_individual():
    return (randint(-y, y+1), randint(-y, y+1))


def is_individual(p):
    return isinstance(p, tuple) and isinstance(p[0], int) and isinstance(p[1], int)


def crossover(p1, p2):
    assert is_individual(p1), is_individual(p2)
    child1 = (p1[0], p2[1])
    child2 = (p2[0], p1[1])
    return [child1, child2]


def mutation(p):
    assert is_individual(p)
    child = (p[1], p[0])
    return child


w1, w2 = -2, 1
y = 120

population = list()
for i in range(POPULATION_SIZE):
    population.append(generate_individual())

for i in range(EVOLUTION_CYCLE):
    prev_sum_of_fitnesses = sum([fitness(x) for x in population])
    parents = find_maxes(population, cnt = BEST_PARENTS_COUNT)
    children = [mutation(p) for p in parents]
    
    for p1 in parents:
        for p2 in parents:
            if p1 != p2:
                cross = crossover(p1, p2)
                for ch in cross:
                    if ch not in children:
                        children.append(ch)
    
    for child in children:    
        if child not in population:
            assert is_individual(child)
            population.append(child)

    population = find_maxes(population, POPULATION_SIZE)

    sum_of_fitnesses = sum([fitness(x) for x in population])

    if prev_sum_of_fitnesses == sum_of_fitnesses:
        population.append(generate_individual())
        population = find_maxes(population, POPULATION_SIZE)

superhero = find_maxes(population)[0]
print("superhero", superhero, fitness(superhero))