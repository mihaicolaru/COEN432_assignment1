# Mihai Olaru 40111734 Amir Cherif 40047635

import random
import copy
import matplotlib.pyplot as plt

import signal
import sys

# Define Square Piece object
class Piece():
    def __init__(self, id, top, right, down, left):
        self.id = id
        self.top = top
        self.right = right
        self.down = down
        self.left = left

    # Apply Rotation to Piece: turn by + or - (clockwise or counter clockwise)
    def turn(self, n):
        top = self.top
        right = self.right
        down = self.down
        left = self.left

        # No rotation applied
        if n == 0:
            pass
        # 90 deg Clockwise Rotation applied
        if n == 1 or n == -3:
            self.top = left
            self.right = top
            self.down = right
            self.left = down
        # 180 deg Clockwise Rotation applied
        if n == 2 or n == -2:
            self.top = down
            self.right = left
            self.down = top
            self.left = right
        # 270 deg Clockwise Rotation applied
        if n == 3 or n == -1:
            self.top = right
            self.right = down
            self.down = left
            self.left = top

    # Display Square Piece (used for debugging)
    def show_piece(self):
        print("piece ", self.id, ": ", self.top, self.right, self.down, self.left)

# Define Individual Solution object            
class Solution():
    def __init__(self, seed=None, generation=0):
        # print("creating new solution")
        self.row_mismatch = 0
        self.col_mismatch = 0
        self.score = 0
        self.generation = generation
        self.chromosome = [] # set of pieces

        if seed is not None:
            self.chromosome = seed

    # randomize the chromosome
    # used to mutate the chromosome(noise)
    # used for population initialization
    def randomize(self, mutaion_rate=0.05):
        random.shuffle(self.chromosome)
        # fill the chromosome with pieces at shuffled locations, 
        # with possible rotations (dependant on mutation rate)
        for piece in self.chromosome:
            if random.random() < mutation_rate:
                piece.turn(random.randint(-3, 3))                
    
    # Display Individual (used for debugging)
    def show_solution(self):
        print("\nsolution: ")
        x = 0
        for piece in self.chromosome:
            if piece == None:
                print("none piece")
                x += 1
            else:
                print("spot: ", x)
                piece.show_piece()
                x += 1
        print("score: ", self.score)

    # compute fitness of the individual
    def fitness(self):
        sum_row = 0
        sum_col = 0
        # count column and row mismatch
        for i in range(len(self.chromosome)):
            # skip every 8th piece
            if (i+1) % 8 != 0:
                if self.chromosome[i].right != self.chromosome[i+1].left:
                    sum_row += 1
            # skip last row
            if i < 55:
                if self.chromosome[i].down != self.chromosome[i+8].top:
                    sum_col += 1
        # sum of row and column mismatch
        self.row_mismatch = sum_row
        self.col_mismatch = sum_col
        self.score = sum_row + sum_col + 1

    # Order 1 crossover implementation
    def crossover(self, other_solution, cross_rate):
        # crossover only if rate is met
        # otherwise return the parents
        if random.random() < cross_rate:  
            # create copy of parents (to avoid modifying the original parents)
            # Avoid shallow copy (copy.copy) as it will copy the reference to the object
            child1 = copy.deepcopy(self)
            child1.generation = self.generation + 1
            child2 = copy.deepcopy(other_solution)
            child2.generation = self.generation + 1

            # pick 2 crossover points in the chromosome (Choose an arbitrary part from the first parent)
            crossover1 = random.randint(0, len(self.chromosome)-2)
            crossover2 = random.randint(crossover1+1, len(self.chromosome)-1)
            segment1 = self.chromosome[crossover1:crossover2]
            segment2 = other_solution.chromosome[crossover1:crossover2]

            used_ids1 = set()
            used_ids2 = set()

            # identify the used pieces in each segment
            for i in range(len(segment1)):
                used_ids1.add(segment1[i].id)
                used_ids2.add(segment2[i].id)
            
            # Copy the numbers that are not in the first part, to the first child
            # - starting right from cut point of the copied part,
            # - using the order of the second parent and wrapping around at the end
            index1 = crossover2
            index2 = crossover2
            for i in range(crossover2, len(self.chromosome)):
                while other_solution.chromosome[index1].id in used_ids1:
                    index1 = (index1+1) % 64
                child1.chromosome[i] = other_solution.chromosome[index1]
                index1 = (index1+1) % 64
                
                while self.chromosome[index2].id in used_ids2:
                    index2 = (index2+1) % 64
                child2.chromosome[i] = self.chromosome[index2]
                index2 = (index2+1) % 64

            for i in range(crossover1):
                while other_solution.chromosome[index1].id in used_ids1:
                    index1 = (index1+1) % 64
                child1.chromosome[i] = other_solution.chromosome[index1]
                index1 = (index1+1) % 64

                while self.chromosome[index2].id in used_ids2:
                    index2 = (index2+1) % 64
                child2.chromosome[i] = self.chromosome[index2]
                index2 = (index2+1) % 64

            # Assess children fitness
            child1.fitness()
            child2.fitness()

            # create new generation copy of parents (could maybe just update generation?)
            new_parent1 = copy.deepcopy(self)
            new_parent1.generation +=1
            new_parent2 = copy.deepcopy(other_solution)
            new_parent2.generation +=1

            # Survivor selection (tournament k=4)
            candidates = [new_parent1, new_parent2, child1, child2]
            # Sorting the candidates based on their fitness score
            candidates = sorted(candidates, key=lambda candidates: candidates.score)
            # pick best 2 out of children and parents
            children = candidates[0:2]

        else: # just return the parents
            new_parent1 = copy.deepcopy(self)
            new_parent1.generation +=1

            new_parent2 = copy.deepcopy(other_solution)
            new_parent2.generation +=1
            children = [new_parent1, new_parent2]

        return children

    # mutate the individual using mutation rate
    def mutation(self, rate):
        # Scramble mutation (randomize the chromosome)
        # Used to maintain diversity in the population
        # helps avoid local minima
        if random.random() < rate:
            self.randomize()
        else: # otherwise mutate a random piece
            for i in range(len(self.chromosome)):
                if random.random() < rate: 

                    self.chromosome[i].turn(random.randint(-3, 3))

# Define Genetic Algorithm object
class Genetic_algorithm():
    def __init__(self, population_size):
        # user defined population size
        self.population_size = population_size
        # current population
        self.population = []
        # overall top solution
        self.top_solution = None
        # track the average score of the population
        self.solution_track = []
        # track the best score of the population
        self.best_solution_track = []

    # initialize population
    def initialize_population(self, seed):
        initial_solution = Solution(seed)

        # create copy of initial solution (otherwise they all get modified in the same way)
        for i in range(self.population_size):
            sol = copy.deepcopy(initial_solution)
            sol.randomize()
            self.population.append(sol)
    
    # order population by score
    def order_population(self):
        self.population = sorted(self.population, key=lambda population: population.score)
        
    # update top solution if a better one is found
    def compute_top(self, solution):
        if solution.score < self.top_solution.score:
            self.top_solution = solution

    # computes generation total fitness
    def overall_score(self):
        sum = 0
        for solution in self.population:
            sum += solution.score
        return sum
    
    # Roulette wheel selection
    def select_parent(self, overall_score):
        parent = -1
        # High quality solutions more likely to be selected
        # even worst in current population usually has non-zero 
        # probability of being selected.
        rand = random.random() * overall_score
        sum = 0
        i = 0
        while i < len(self.population) and sum < rand:
            sum += self.population[i].score
            parent += 1
            i += 1
        return parent
    
    # show curren generation information
    def display(self):
        print("Generation: ", self.population[0].generation)
        print("Current Best Score: ", self.population[0].score)
        print("Overall Best Score: ", self.top_solution.score, " generation: ", self.top_solution.generation)
        print("Current Average Score: ", (self.overall_score()/self.population_size))

    # evolve the population (parent selection, crossover, mutation, survivor selection)
    def evolve(self, mutation_rate, cross_rate, reassess_rate, num_gens, seed):
        # save original rates
        omr = mutation_rate
        ocr = cross_rate
        print("\n\n================= init population =================")
        # initialize population
        self.initialize_population(seed)
        # compute fitness of initial population
        for solution in self.population:
            solution.fitness()
        # order population by score
        self.order_population()
        # compute top solution
        self.top_solution = self.population[0]
        # show current generation stats
        self.display()

        print("\n\n================= start evolving =================")
        # iterate to evolve over the number of generations
        for generation in range(num_gens):
            # compute generation total fitness
            sum = self.overall_score()
            new_population = []
            # Reassess mutation and crossover rates every specific number of generations
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Please Note:
            # Crossover & Mutation play different roles in the GA depending on:
            # -> The Phase of Evolution 
            # -> Diversity of the population
            # => Below we try to adjust the rates based on the current phase of evolution
            # => Initial rates selected based on experimentation 
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if generation != 0 and generation % (reassess_rate) == 0:
                print("\n\n#######################################################################################")
                print("\nadjusting rates")
                # compute average of previous reassess_rate generations
                prev_gen = self.solution_track[-reassess_rate:]
                prev_avg = 0
                for i in range(len(prev_gen)):
                    prev_avg += prev_gen[i]
                prev_avg = prev_avg / reassess_rate

                print("average of previous ", reassess_rate, " generation scores: ", prev_avg)
                print("current population score: ", sum)

                # if current result better than current avg by 3% or more
                if (prev_avg - sum) > (0.01 * prev_avg):
                    print("no change in rates")
                else:
                    # current result same or worse than current avg by 2%
                    print("increase mutation, decrease crossover")
                    mutation_rate *= 1.02
                    cross_rate /= 1.02

                    if sum/self.population_size > (2 * self.top_solution.score):
                        print("resetting mutation and crossover rate")
                        mutation_rate = omr
                        cross_rate = ocr 
                print("new mutation", mutation_rate*100,"\ncrossover: ", cross_rate*100)

                print("\n#######################################################################################")

            # Iterate over the population to create next generation
            for new_solutions in range(0, self.population_size, 2):
                # select parents using roulette wheel selection
                parent1 = self.select_parent(sum)
                parent2 = self.select_parent(sum)
                # crossover using order 1 crossover and rate of crossover
                children = self.population[parent1].crossover(self.population[parent2], cross_rate)
                child1 = children[0] 
                child2 = children[1]
                # mutate children using mutation rate
                child1.mutation(mutation_rate)
                child2.mutation(mutation_rate)
                # add children to new population
                new_population.append(child1)
                new_population.append(child2)

            print("\n\n================= new generation =================") 
            self.population = new_population
            # compute fitness of new population
            for solution in self.population:
                solution.fitness()
            # order population by score
            self.order_population()
            # update best overall solution
            self.compute_top(self.population[0])                
            # track the average score of the population
            self.solution_track.append(sum)
            # track the best score of the population
            self.best_solution_track.append(self.top_solution.score)
            # show current generation stats
            self.display()       
        print("top solution score: ", self.top_solution.score)
        return self.top_solution


# detect early termination, return current best solution
def program_exit(sig, frame):
    print("\n\nGA terminated early, returning current best solution")

    # use current best solution
    solution_found = GA.top_solution

    print("solution found on generation: ", solution_found.generation, "\nscore: ", solution_found.score)
    # display final solution
    solution_found.show_solution()

    # write solution to file
    foutput = open("Ass1Output.txt", "w")
    solution_str = "Mihai Olaru 40111734 Amir Cherif 40047635\n"
    for i in range(len(solution_found.chromosome)):
        piece = str(solution_found.chromosome[i].top) + str(solution_found.chromosome[i].right) + str(solution_found.chromosome[i].down) + str(solution_found.chromosome[i].left)
        if i == 63:
            break
        if (i + 1) % 8 == 0:
            solution_str += piece + "\n"
        else:
            solution_str += piece + " "
    solution_str += piece
    foutput.write(solution_str)
    foutput.close()

    # plot the average and best score of the population over the generations so far
    plt.plot(list(range(len(GA.best_solution_track))), GA.best_solution_track, label = "Best Score")
    # compute average score over lifetime of the population
    avg_score = []
    for i in range(len(GA.solution_track)):
        avg_score.append(GA.solution_track[i]/population_size)
    # plot the average score
    plt.plot(list(range(len(GA.solution_track))), avg_score, label = "Average Score")
    # naming the x axis 
    plt.xlabel('Generation')
    # naming the y axis 
    plt.ylabel('Mismatches')
    # show a legend on the plot 
    plt.legend()
    # function to save to file
    plt.savefig('Ass1Lifetime.png')

    sys.exit(0)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       Driver Code     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# register function on early program termination signal
signal.signal(signal.SIGINT, program_exit)

# Read the original square pieces from Input file
finput = open("Ass1Input.txt", "r")
seed = []
# read 64 pieces
for i in range(0, 64):
    seed.append(Piece(i, finput.read(1), finput.read(1), finput.read(1), finput.read(1)))
    finput.read(1)
finput.close()

# User defined parameters
population_size = int(input("enter population size: "))
number_generations = int(input("enter number of generations: "))

# convert mutation and crossover rates from percentages to float
# Please Note: Initial rates selected based on experimentation 
mutation_rate = 0.1/100
cross_rate = 100/100

# adjust reassess rate based on number of generations
# Please Note: Current phase of evolution selected based on experimentation
if number_generations < 100:
    reassess_rate = 10
elif number_generations < 500:
    reassess_rate = 50
else:
    reassess_rate = 100
print("Reassess Rate: ", reassess_rate)
# create GA object
GA = Genetic_algorithm(population_size)

# if terminated early, raise keyboard interrupt signal
try:
    # evolve the population
    solution_found = GA.evolve(mutation_rate, cross_rate, reassess_rate, number_generations, seed)
    # display final solution
    solution_found.show_solution()

    # write solution to file
    foutput = open("Ass1Output.txt", "w")
    solution_str = "Mihai Olaru 40111734 Amir Cherif 40047635\n"
    for i in range(len(solution_found.chromosome)):
        piece = str(solution_found.chromosome[i].top) + str(solution_found.chromosome[i].right) + str(solution_found.chromosome[i].down) + str(solution_found.chromosome[i].left)
        if i == 63:
            break
        if (i + 1) % 8 == 0:
            solution_str += piece + "\n"
        else:
            solution_str += piece + " "
    solution_str += piece
    foutput.write(solution_str)
    foutput.close()

    # plot the average and best score of the population over the generations
    plt.plot(list(range(number_generations)), GA.best_solution_track, label = "Best Score")
    # compute average score over lifetime of the population
    avg_score = []
    for i in range(len(GA.solution_track)):
        avg_score.append(GA.solution_track[i]/population_size)
    # plot the average score
    plt.plot(list(range(number_generations)), avg_score, label = "Average Score")
    # naming the x axis 
    plt.xlabel('Generation')
    # naming the y axis 
    plt.ylabel('Mismatches')
    # show a legend on the plot 
    plt.legend()
    # function to save to file
    plt.savefig('Ass1Lifetime.png')

except KeyboardInterrupt:
    print("ctrl+c pressed, exciting...")