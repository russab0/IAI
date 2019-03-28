from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngImageFile
from random import randint
from os import mkdir
from datetime import datetime


INF = 10**9
POPULATION_SIZE = 10
EVOLUTION_CYCLE = 100
BEST_PARENTS_COUNT = 3
FITNESS_BLOCK_SIZE = 8
SWAP_BLOCK_SIZE = 8
IMAGE_SIZE = 512
COPY_BLOCK_SIZE = 16

perferct_image = None
input_image = None

class Picture():
    image = None
    __fitness__ = None

    def __init__(self, image):
        self.image = image

    def get_fitness(self):
        if self.__fitness__ is not None:
            return self.__fitness__
        
        perfect = perfect_image
        first = self.image.load()
        second = perfect.image.load()
        result = 0
        
        for i in range(0, IMAGE_SIZE):
            for j in range(0, IMAGE_SIZE):
                
                for t in range(3):
                    result += abs(first[i, j][t] - second[i, j][t])

        self.__fitness__ = result
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
    perfect = perfect_image.image
    first = p1.image
    second = p2.image

    first_pix = first.load()
    second_pix = second.load()   
    perfect_pix = perfect.load()
    
    child = first.copy()
    child_draw = ImageDraw.Draw(child)
    
    for i in range(0, IMAGE_SIZE):
        for j in range(0, IMAGE_SIZE):
            
            rgb = [0, 0, 0]
            
            for t in range(3):
                a = abs(perfect_pix[i, j][t] - first_pix[i, j][t])
                b = abs(perfect_pix[i, j][t] - second_pix[i, j][t])
                
                if a < b:
                    rgb[t] = first_pix[i, j][t]
                else:
                    rgb[t] = second_pix[i, j][t]
                    
            child_draw.point((i, j), (rgb[0], rgb[1], rgb[2]))

    return Picture(child)


def mutation(p):
    perfect = perfect_image.image
    p = p.image
    
    perfect_pix = perfect.load() 
    
    p_draw = ImageDraw.Draw(p)
    
    for t in range(10):
        x = randint(0, 512/COPY_BLOCK_SIZE - 1) * COPY_BLOCK_SIZE
        y = randint(0, 512/COPY_BLOCK_SIZE - 1) * COPY_BLOCK_SIZE
        
        for i in range(COPY_BLOCK_SIZE):
            for j in range(COPY_BLOCK_SIZE):        
                p_draw.point((i + x, j + y), perfect_pix[i + x, j + y])
    
    return Picture(p)


def generate_individual(p):
    first = p.image.copy()
    second = p.image.copy()
    
    first_draw = ImageDraw.Draw(first) #Создаем инструмент для рисования. 
    first_pix = first.load() #Выгружаем значения пикселей.

    second_draw = ImageDraw.Draw(second) #Создаем инструмент для рисования. 
    second_pix = second.load()     #Выгружаем значения пикселей.
    
    #make 100 random permutations
    for t in range(1000):
        
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

perfect_image = Picture(Image.open("perfect\\cat.jpg")) #Открываем изображение
input_image = Picture(Image.open("input\\smeshariki.jpg")) #Открываем изображение


population = [input_image]
for i in range(POPULATION_SIZE - 1):
    population.append(generate_individual(input_image))

def append_individual(ind):
    global population
    population.append(ind)
    population.sort(key = lambda x : x.get_fitness())
    population = find_bests(population, POPULATION_SIZE)
    
folder = str(datetime.now().strftime('day %d %H.%M'))
mkdir(folder)
for i in range(len(population)):
    population[i].image.save(folder + "\\init_pop" + str(i) + ".jpg", "JPEG")
print([x.get_fitness() for x in population])
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
                children += [crossover(p1, p2)]

    print("childs", [id(x) for x in children])
    for child in children:    
        if child not in population:
            append_individual(child)

    population = find_bests(population, POPULATION_SIZE)

    """sum_of_fitnesses = sum([fitness(x) for x in population])
    if prev_sum_of_fitnesses == sum_of_fitnesses:
        population.append(generate_individual())
        population = find_maxes(population, POPULATION_SIZE)"""


    superhero = population[0]
    print("superhero", superhero.get_fitness())
    #print("total fitness", sum([x.get_fitness() for x in population]))
    #print("fitness population", population)
    #print("id of population", [id(x) for x in population])
    print()
    superhero.image.save(folder + "\\iter" + str(i) + ".jpg", "JPEG")


superhero = population[0]
superhero.image.save(folder + "superhero.jpg", "JPEG")