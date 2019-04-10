from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngImageFile
from random import randint
from os import mkdir
from datetime import datetime
from gc import collect

INF = 10**18
IMAGE_SIZE = 512
POPULATION_SIZE = 15
EVOLUTION_CYCLE = 255
BEST_PARENTS_COUNT = 4
MUTATION_BLOCK_SIZE = 8      ;  MUTATION_CYCLE = 100
CROSSOVER_BLOCK_SIZE = 16    ;  CROSSOVER_CYCLE = 100
GENERATION_BLOCK_SIZE = 128  ;  GENERATION_CYCLE = 10

CONSTS = {'INF': INF, 
    'IMAGE_SIZE': IMAGE_SIZE, 
    'POPULATION_SIZE': POPULATION_SIZE, 
    'EVOLUTION_CYCLE': EVOLUTION_CYCLE, 
    'BEST_PARENTS_COUNT': BEST_PARENTS_COUNT,
    'MUTATION_BLOCK_SIZE': MUTATION_BLOCK_SIZE, 
    'CROSSOVER_BLOCK_SIZE': CROSSOVER_BLOCK_SIZE, 
    'GENERATION_BLOCK_SIZE': GENERATION_BLOCK_SIZE,
    'MUTATION_CYCLE': MUTATION_CYCLE, 
    'CROSSOVER_CYCLE': CROSSOVER_CYCLE, 
    'GENERATION_CYCLE': GENERATION_CYCLE}
    
assert MUTATION_BLOCK_SIZE <= IMAGE_SIZE
assert CROSSOVER_BLOCK_SIZE <= IMAGE_SIZE
assert GENERATION_BLOCK_SIZE <= IMAGE_SIZE
assert BEST_PARENTS_COUNT <= POPULATION_SIZE


perfect_image = None
base_image = None
population = list()


# Class for storing an image and its fitness function value
class Picture():
    __image__ = None
    __fitness__ = None

    # Initializes Picture by given ImageFile
    def __init__(self, image, fitness = None):
        self.__image__ = image
        self.__fitness__ = fitness

    # Returns pixels of the Picture
    def load(self):
        return self.__image__.load()

    # Returns drawable object based on the image
    def draw(self): 
        return ImageDraw.Draw(self.__image__)

    # Copies current Picture and returns it
    def copy(self):
        return Picture(self.__image__.copy(), None)

    # Saves the picture by given directory and extension
    def save(self, directory, ext):
        return self.__image__.save(directory, ext)

    # Returns fitness function of the Picture
    def get_fitness(self):
        if self.__fitness__ is not None: # If it is already calculated
            return self.__fitness__
        
        ind_pix = self.load()
        perf_pix = perfect_image.load()
        fit = 0
        
        # For all pixels and for all 3 color-parameters in RGB-model
        # sums absolute difference between the picture and perfect picture
        for i in range(0, IMAGE_SIZE):
            for j in range(0, IMAGE_SIZE):
                #print(ind_pix[i,j])
                #print(perf_pix[i,j])
                fit += sum([abs(ind_pix[i,j][t] - perf_pix[i,j][t]) 
                                for t in range(3)])

        self.__fitness__ = fit
        return fit


# Changes some genes in the individual and returns new child
def mutation(ind):
    ind = ind.copy()
    ind_draw = ind.draw()
    perf_pix = perfect_image.load()

    for _ in range(MUTATION_CYCLE):
        # Selecting random coordinates as a left-top pixel of the block
        x = randint(0, IMAGE_SIZE - MUTATION_BLOCK_SIZE - 1)
        y = randint(0, IMAGE_SIZE - MUTATION_BLOCK_SIZE - 1)
        ind_pix = ind.load()

        # Calculating the best rgb for the block
        best_score = INF
        best_rgb = tuple(ind_pix[x, y])
        for q in range(100):
            # Generating random rgb tuple
            rgb = tuple([randint(0, 10) * 25 for _ in range(3)])
            score = 0
            for i in range(x, x + MUTATION_BLOCK_SIZE):
                for j in range(y, y + MUTATION_BLOCK_SIZE):
                    score += sum([
                        abs(perf_pix[i,j][color] - rgb[color]) 
                        for color in range(3)])
            if score < best_score:
                best_score = score
                best_rgb = rgb

        # Drawing the best generated rgb color on the block
        for i in range(x, x + MUTATION_BLOCK_SIZE):
            for j in range(y, y + MUTATION_BLOCK_SIZE):
                ind_draw.point((i, j), best_rgb)
    
    return ind


# Gets two parents as arguments and returns child 
# which has the best genes of both parents
def crossover(first, second):
    first_pix = first.load()
    second_pix = second.load()   
    perfect_pix = perfect_image.load()
    
    child = first.copy()
    child_draw = child.draw() 
     
    for _ in range(CROSSOVER_CYCLE):
        # Selecting random coordinates as a left-top pixel of the block
        x = randint(0, IMAGE_SIZE - CROSSOVER_BLOCK_SIZE - 1)
        y = randint(0, IMAGE_SIZE - CROSSOVER_BLOCK_SIZE - 1)
        for i in range(x, x + CROSSOVER_BLOCK_SIZE):
            for j in range(y, y + CROSSOVER_BLOCK_SIZE):
                # Selecting the best rgb from parents
                rgb = [0] * 3
                for t in range(3):
                    # Calculating absolute distances from parents to perfect image
                    a = abs(perfect_pix[i, j][t] - first_pix[i, j][t])
                    b = abs(perfect_pix[i, j][t] - second_pix[i, j][t])
                    if a < b:
                        rgb[t] = first_pix[i, j][t]
                    else:
                        rgb[t] = second_pix[i, j][t]
                # Drawing the best rgb
                child_draw.point((i, j), tuple(rgb))

    return child


# Returns cnt number of best individuals from population
def find_bests(population, cnt = 1):
    return population[:cnt]


# Generates individual based on base picture
def generate_individual(base):
    ind = base.copy()
    ind_draw = ind.draw()
    ind_pix = ind.load() 
    
    for _ in range(GENERATION_CYCLE):    
        # Selecting coordinates for the first block
        x1 = randint(0, IMAGE_SIZE - 1 - GENERATION_BLOCK_SIZE)
        y1 = randint(0, IMAGE_SIZE - 1 - GENERATION_BLOCK_SIZE)
        # Selecting coordinates for the second block
        x2 = randint(0, IMAGE_SIZE - 1 - GENERATION_BLOCK_SIZE)
        y2 = randint(0, IMAGE_SIZE - 1 - GENERATION_BLOCK_SIZE)
        
        for i in range(GENERATION_BLOCK_SIZE):
            for j in range(GENERATION_BLOCK_SIZE):
                # Swapping pixels of first and second block
                first_coord = (x1 + i, y1 + j)
                second_coord = (x2 + i, y2 + j)
                temp = ind_pix[first_coord]
                ind_draw.point(first_coord, ind_pix[second_coord])
                ind_draw.point(second_coord, temp)
                
    return ind


# Appends given individual to population 
# and kills most weak members of population
def append_individual(ind):
    global population
    population.append(ind)
    population.sort(key = lambda x : x.get_fitness())
    population = find_bests(population, POPULATION_SIZE)


def main(base, perfeсе):
    global base_image, perfect_image, population

    # Opening images
    base_image = Picture(Image.open("images\\" + base + ".jpg"))
    perfect_image = Picture(Image.open("images\\" + perfect + ".jpg"))
    folder = str(datetime.now().strftime('day %d %H.%M.%S'))
    mkdir(folder)

    # Writing used constants to the info-file
    const_file = open(folder + "\\info.txt", "w")
    for name, value in CONSTS.items():
        print(name, value, file=const_file)
    const_file.close()

    # Creating initial population
    population = [base_image]
    for i in range(POPULATION_SIZE - 1):
        population.append(generate_individual(base_image))
        population[i].save(folder + "\\init_pop" + str(i) + ".jpg", "JPEG")
    population.sort(key=lambda x: x.get_fitness())
    
    # 0-th iteration's superhero is strongers individual from initial population
    population[0].save(folder + "\\iter 0.jpg", "JPEG")
    fit_file = open(folder + "\\fitness.txt", "w")
    print(population[0].get_fitness(), file=fit_file)

    for i in range(1, EVOLUTION_CYCLE + 1):
        print("iter", i)
        # Caclulatinf summ of all fitnesses of population member
        prev_total_fitness = sum([x.get_fitness() for x in population])
        # Selecting the strongest parents from population
        parents = find_bests(population, cnt=BEST_PARENTS_COUNT)
        # Creating list of mutated parents
        children = [mutation(p) for p in parents]
        
        # Crossovering best parents
        for p1 in parents:
            for p2 in parents:
                # Parents should not be the same
                if p1 != p2:
                    children.append(crossover(p1, p2))
                    
        # Appending created children to population                    
        for child in children:    
            # We do not need the same individuals in population
            if child not in population: 
                append_individual(child)

        # If current iteration did not improve total fitness
        # then generate new individual
        total_fitness = sum([x.get_fitness() for x in population])
        while prev_total_fitness == total_fitness:
            population.append(generate_individual(population[0]))
            total_fitness = sum([x.get_fitness() for x in population])

        # Saving superhero to the file
        superhero = population[0]
        superhero.save(folder + "\\iter" + str(i) + ".jpg", "JPEG")
        print(superhero.get_fitness(), file=fit_file)
            
    fit_file.close()

#tests = [("icarus", "airplane"),
#        ("black-square", "star"),
#        ("dr-house", "house")]

tests = [
        ("dr-octopus", "piter-parker"),
        ("buildings", "city")]
    

for base, perfect in tests:
    main(base, perfect)
    collect()
    perfect_image = None
    base_image = None
    population = list()