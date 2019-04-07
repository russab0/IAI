from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngImageFile
from random import randint
from os import mkdir
from datetime import datetime


INF = 10**18
IMAGE_SIZE = 512
POPULATION_SIZE = 10
EVOLUTION_CYCLE = 100
BEST_PARENTS_COUNT = 4
SWAP_BLOCK_SIZE = 32
FITNESS_BLOCK_SIZE = 8
MUTATION_BLOCK_SIZE = 8


input_image = None
base_image = None
population = list()



class Picture():
    image = None
    __fitness__ = None

    def __init__(self, image):
        self.image = image

    def get_fitness(self):
        if self.__fitness__ is not None:
            return self.__fitness__
        
        perfect = input_image
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

def crossover(p1, p2):
    perfect = input_image.image
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


def mutation(ind):
    ind = ind.image.copy()
    ind_draw = ImageDraw.Draw(ind)

    perfect = input_image.image
    perfect_pix = perfect.load()

    for t in range(100):
        x = randint(0, IMAGE_SIZE - 1 - MUTATION_BLOCK_SIZE)
        y = randint(0, IMAGE_SIZE - 1 - MUTATION_BLOCK_SIZE)
        
        ind_pix = ind.load()

        best_score = INF
        best_rgb = ind_pix[x, y]

        for q in range(100):
            r, g, b = [randint(0, 10) * 25 for _ in range(3)]
            
            score = 0
            for i in range(MUTATION_BLOCK_SIZE):
                for j in range(MUTATION_BLOCK_SIZE):
                    score += sum([abs(perfect_pix[x+i, y+j][color] - [r, g, b][color]) for color in range(3)])
            if score < best_score:
                best_score = score
                best_rgb = (r, g, b)

        for i in range(MUTATION_BLOCK_SIZE):
            for j in range(MUTATION_BLOCK_SIZE):
                ind_draw.point((x+i, y+j), best_rgb)
    
    return Picture(ind)


def generate_individual(p):
    first = p.image.copy()
    
    first_draw = ImageDraw.Draw(first)
    first_pix = first.load() 
    
    #make 100 random permutations
    for t in range(100):    
        #choose block 8x8 from 512x512 matrix
        x1 = randint(0, IMAGE_SIZE - 1 - SWAP_BLOCK_SIZE)
        y1 = randint(0, IMAGE_SIZE - 1 - SWAP_BLOCK_SIZE)
        #choose another block 8x8 from 512x512 matrix
        x2 = randint(0, IMAGE_SIZE - 1 - SWAP_BLOCK_SIZE)
        y2 = randint(0, IMAGE_SIZE - 1 - SWAP_BLOCK_SIZE)
        
        for i in range(SWAP_BLOCK_SIZE):
            for j in range(SWAP_BLOCK_SIZE):
                #print(i, x1, j, y1)
                temp = first_pix[i + x1, j + y1]
                first_draw.point((i + x1, j + y1), first_pix[i + x2, j + y2])
                first_draw.point((i + x2, j + y2), temp)
                
    return Picture(first) # or first and second


def append_individual(ind):
    global population
    population.append(ind)
    population.sort(key = lambda x : x.get_fitness())
    population = find_bests(population, POPULATION_SIZE)


input_image = Picture(Image.open("images\\harold.jpg")) #Открываем изображение
base_image = Picture(Image.open("images\\vangogh.jpg")) #Открываем изображение
folder = str(datetime.now().strftime('day %d %H.%M'))
mkdir(folder)


population = [base_image]
for i in range(POPULATION_SIZE - 1):
    population.append(generate_individual(base_image))

for i in range(len(population)):
    population[i].image.save(folder + "\\init_pop" + str(i) + ".jpg", "JPEG")
population.sort(key = lambda x: x.get_fitness())

for i in range(EVOLUTION_CYCLE):
    print("iter", i)
    #prev_sum_of_fitnesses = sum([fitness(x, input_image) for x in population])
    parents = find_bests(population, cnt = BEST_PARENTS_COUNT)
    children = [mutation(p) for p in parents]
    
    for p1 in parents:
        for p2 in parents:
            if p1 != p2:
                children += [crossover(p1, p2)]

    for child in children:    
        if child not in population:
            append_individual(child)

    population = find_bests(population, POPULATION_SIZE)

    #sum_of_fitnesses = sum([fitness(x) for x in population])
    #if prev_sum_of_fitnesses == sum_of_fitnesses:
    #    population.append(generate_individual())
    #    population = find_maxes(population, POPULATION_SIZE)

    superhero = population[0]
    superhero.image.save(folder + "\\iter" + str(i) + ".jpg", "JPEG")
