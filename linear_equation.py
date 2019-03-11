"""Exercise: Solve Linear Equation using GA

-- Compose a simple (2-3 weights) linear equation, e.g. y = w1*x1 + w2*x2
-- Create a test and a validation set. Each of them should have 
set of values of x1, x2, y (for the former example) – an array of examples
-- Code a genetic algorithm that tries to find the best w1, w2 that minimize
the error"""

from random import randint

INF = 10**9
w1, w2 = 2, 3
y = 12

def fitness(X):
    x1, x2 = X
    a, b = x1 * w1 + x2 * w2, y
    a, b = min(a, b), max(a, b)
    return a / b * 100

population = list()
for i in range(3):
    population.append((randint(-y, y+1), randint(-y, y+1)))
    
print(population)
print(fitness((4, 2)))

def find_2_maxes(arr):
    q = sorted(arr, key = lambda x: fitness(x))
    return (q[-2], q[-1])

# Crossover:
for i in range(100):
    p1, p2 = find_2_maxes(population)
    child1 = (p1[0], p2[1])
    child2 = (p2[0], p1[1])
    population.append(child1)
    population.append(child2)
    print(fitness(child1), fitness(child2))

superhero = find_2_maxes(population)[-1]
print(superhero, fitness(superhero))