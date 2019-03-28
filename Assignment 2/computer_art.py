from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngImageFile
from random import randint
from random import randint


INF = 10**9
POPULATION_SIZE = 10
EVOLUTION_CYCLE = 100
BEST_PARENTS_COUNT = 3
FITNESS_BLOCK_SIZE = 8
SWAP_BLOCK_SIZE = 8
IMAGE_SIZE = 512

class Picture():
    image = None
    fitness = None

    def __init__(self, image):
        self.image = image

    def get_fitness(self):
        perfect =perfect_image
        if self.fitness is not None:
            return self.fitness
        first = self.image.copy().load()

        second = perfect.image.copy().load()
        result = 0
        for i in range(0, IMAGE_SIZE, FITNESS_BLOCK_SIZE):
            for j in range(0, IMAGE_SIZE, FITNESS_BLOCK_SIZE):
                sumr1 = sumg1 = sumb1 = sumr2 = sumg2 = sumb2 = 0
                
                for sx in range(FITNESS_BLOCK_SIZE):
                    for sy in range(FITNESS_BLOCK_SIZE):
                        x = i + sx
                        y = j + sy
                        
                        sumr1 += first[x, y][0]
                        sumg1 += first[x, y][1]
                        sumb1 += first[x, y][2]
                        sumr2 += second[x, y][0]
                        sumg2 += second[x, y][1]
                        sumb2 += second[x, y][2]
                        
                meanr1 = sumr1/64.0
                meang1 = sumg1/64.0
                meanb1 = sumb1/64.0
                meanr2 = sumr2/64.0
                meang2 = sumg2/64.0
                meanb2 = sumb2/64.0
                
                varr1 = varg1 = varb1 = 0
                varr2 = varg2 = varb2 = 0
                
                for sx in range(FITNESS_BLOCK_SIZE):
                    for sy in range(FITNESS_BLOCK_SIZE):
                        x = i + sx
                        y = j + sy
                        
                        varr1 += (first[x, y][0] - meanr1)**2
                        varg1 += (first[x, y][1] - meang1)**2
                        varb1 += (first[x, y][2] - meanb1)**2
                        varr2 += (second[x, y][0] - meanr2)**2
                        varg2 += (second[x, y][1] - meang2)**2
                        varb2 += (second[x, y][2] - meanb2)**2
                        
                varr1 = varr1 / 64.0
                varg1 = varg1 / 64.0
                varb1 = varb1 / 64.0
                varr2 = varr2 / 64.0
                varg2 = varg2 / 64.0
                varb2 = varb2 / 64.0
                
                result += abs(varr2 - varr1) + abs(varg2 - varg1) + abs(varb2 - varb1)

        self.fitness = result
        return result



def find_bests(arr, cnt = 1):
    return arr[:cnt]


def get_child(first, second):
    first = first.image
    second = second.image

    
    first_draw = ImageDraw.Draw(first) #Создаем инструмент для рисования. 
    first_pix = first.load() #Выгружаем значения пикселей.

    second_draw = ImageDraw.Draw(second) #Создаем инструмент для рисования. 
    second_pix = second.load()     #Выгружаем значения пикселей.
    
    #make 100 random permutations
    for t in range(100):
        
        #choose block 8x8 from 512x512 matrix
        x1 = randint(0, 512/SWAP_BLOCK_SIZE - 1) * SWAP_BLOCK_SIZE
        y1 = randint(0, 512/SWAP_BLOCK_SIZE - 1) * SWAP_BLOCK_SIZE
        
        #choose another block 8x8 from 512x512 matrix
        x2 = randint(0, 512/SWAP_BLOCK_SIZE - 1) * SWAP_BLOCK_SIZE
        y2 = randint(0, 512/SWAP_BLOCK_SIZE - 1) * SWAP_BLOCK_SIZE   
        
        for i in range(SWAP_BLOCK_SIZE):
            for j in range(SWAP_BLOCK_SIZE):
                #print(i, x1, j, y1)
                temp = first_pix[i + x1, j + y1]
                first_draw.point((i + x1, j + y1), second_pix[i + x2, j + y2])
                second_draw.point((i + x2, j + y2), temp)
                
    return Picture(first) # or first and second


def crossover(p1, p2):
    return get_child(p1, p2)

def mutation(p):
    return get_child(p, p)

def generate_individual(p):
    return mutation(p)

perfect_image = Picture(Image.open("japan.jpg")) #Открываем изображение
input_image = Picture(Image.open("input1.jpg")) #Открываем изображение

population = [input_image]
for i in range(POPULATION_SIZE - 1):
    population.append(mutation(input_image))

def append_individual(ind):
    global population
    population.append(ind)
    population.sort(key = lambda x : x.get_fitness())
    population = find_bests(population, POPULATION_SIZE)
    
print("!!!", type(input_image))
print([type(x) for x in population])
population.sort(key = lambda x: x.get_fitness())

for i in range(EVOLUTION_CYCLE):
    print("iter", i)
    #prev_sum_of_fitnesses = sum([fitness(x, perfect_image) for x in population])
    #assert len()
    parents = find_bests(population, cnt = BEST_PARENTS_COUNT)
    children = [mutation(p) for p in parents]
    
    for p1 in parents:
        for p2 in parents:
            if p1 != p2:
                cross = [crossover(p1, p2)]
                for ch in cross:
                    if ch not in children:
                        children.append(ch)
    print("childs", [id(x) for x in children])
    for child in children:    
        if child not in population:
            append_individual(child)

    print("child vs parent", min([x.get_fitness() for x in children]),
                            max([x.get_fitness() for x in parents]))

    population = find_bests(population, POPULATION_SIZE)

    """sum_of_fitnesses = sum([fitness(x) for x in population])
    if prev_sum_of_fitnesses == sum_of_fitnesses:
        population.append(generate_individual())
        population = find_maxes(population, POPULATION_SIZE)"""


    superhero = find_bests(population)[0]
    print("superhero", superhero.get_fitness())
    print("total fitness", sum([x.get_fitness() for x in population]))
    #print("fitness population", population)
    print("id of population", [id(x) for x in population])
    print()
    superhero.image.save("superhero2.jpg", "JPEG")