# include libraries
import random

# define components

class Piece():
    def __init__(self, id, top, right, down, left):
        self.id = id
        self.top = top
        self.right = right
        self.down = down
        self.left = left

    def turn(self, n):
        top = self.top
        right = self.right
        down = self.down
        left = self.left

        if n == 0:
            pass
        if n == 1 or -3:
            self.top = left
            self.right = top
            self.down = right
            self.left = down
        if n == 2 or -2:
            self.top = down
            self.right = left
            self.down = top
            self.left = right
        if n == 3 or -1:
            self.top = right
            self.right = down
            self.down = left
            self.left = top
            

class Solution():
    def __init__(self, seed):
        self.row_mismatch = 0
        self.col_mismatch = 0
        self.score = 0
        self.generation = 0
        self.chromosome = [None]*64 # set of pieces

        # shuffle index 0-63
        index_scramble = list(range(0,64))

        print(index_scramble)

        random.shuffle(index_scramble)

        print(index_scramble)

        # fill the chromosome with pieces at shuffled locations, with possible rotations
        for piece in seed:
            i = index_scramble.pop()
            if random.random() < 0.05:
                turned_piece = piece
                self.chromosome[i] = turned_piece.turn(random.randint(-3, 3))
            else:
                self.chromosome[i] = piece

        for piece in self.chromosome:
            if piece != None:
                print(piece.top, piece.right, piece.down, piece.left)

    def fitness(self):
        sum_row = 0
        sum_col = 0

        # count column and row mismatch, make this better ?
        for i in range(0, 56):
            if self.chromosome[i].right != self.chromosome[i+1].left:
                sum_row += 1

            if self.chromosome[i].down != self.chromosome[i+8].top:
                sum_col += 1

        for i in range(56, 63):
            if self.chromosome[i].right != self.chromosome[i+1].left:
                sum_row += 1

            if self.chromosome[i].down != self.chromosome[i-56].top:
                sum_col += 1
        
        if self.chromosome[63].right != self.chromosome[0].left:
            sum_row += 1

        if self.chromosome[63].down != self.chromosome[7].top:
            sum_col += 1

        self.row_mismatch = sum_row
        self.col_mismatch = sum_col
        self.score = sum_row + sum_col

    def crossover(self, other_solution):
        pass    # need to implement crossover for permutations

    def mutation(self, rate):
        for i in range(len(self.chromosome)):
            if random.random() < rate: 
                self.chromosome[i].turn(random.randint(-3, 3))
        

class Genetic_algorithm():
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []
        self.generation = 0
        self.top_solution = None
        self.solution_track = []

    def initialize_population(self, seed):
        for i in range(self.population_size):
            self.population.append(Solution(seed))
        
        self.top_solution = self.population[0]
    
    def order_population(self):
        self.population = sorted(self.population, key=lambda population: population.score, reverse=False)
        
    def compute_top(self, solution):
        if solution.score < self.top_solution.score:
            self.top_solution = solution

    def overall_score(self):
        sum = 0
        for solution in self.population:
            sum += solution.score
        return sum
    
    def select_parent(self, overall_score):
        pass

    def display(self):
        pass

    # solve
    def evolve(self, mutation_rate, num_gens, seed):
        self.initialize_population(seed)

        for solution in self.population:
            solution.fitness()

        self.order_population()
        self.top_solution = self.population[0]
        self.solution_track.append(self.top_solution.score)





        return self.top_solution

        

# main
finput = open("Ass1Input.txt", "r")
seed = []
for i in range(0, 64):
    seed.append(Piece(i, finput.read(1), finput.read(1), finput.read(1), finput.read(1)))
    finput.read(1)

for piece in seed:
    print(piece.top, piece.right, piece.down, piece.left)

population_size = int(input("enter population size: "))
number_generations = int(input("enter number of generations: "))
mutation_rate = int(input("enter mutation rate (0-100): "))/100

GA = Genetic_algorithm(population_size)

solution_found = GA.evolve(mutation_rate, number_generations, seed)

