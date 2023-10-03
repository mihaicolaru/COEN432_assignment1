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

    def show_piece(self):
        print("piece ", self.id, ": ", self.top, self.right, self.down, self.left)
            

class Solution():
    def __init__(self, seed):
        # print("creating new solution")
        self.row_mismatch = 0
        self.col_mismatch = 0
        self.score = 0
        self.generation = 0
        self.chromosome = [None]*64 # set of pieces

        # shuffle index 0-63
        index_scramble = list(range(0,64))

        # print(index_scramble)

        random.shuffle(index_scramble)

        # print(index_scramble)

        # fill the chromosome with pieces at shuffled locations, with possible rotations
        for piece in seed:
            i = index_scramble.pop()
            # print("insert in spot ", i)
            # piece.show_piece()

            if random.random() < 0.05:
                # print("turned")
                # piece.show_piece()
                turned_piece = piece
                turned_piece.turn(random.randint(-3, 3))
                self.chromosome[i] = turned_piece
                # turned_piece.show_piece()
            else:
                self.chromosome[i] = piece

        # for piece in self.chromosome:
        #     if piece == None:
        #         print("none piece")
        #     else:
        #         piece.show_piece()

    # def randomize(self):
    #      # shuffle index 0-63
    #     index_scramble = list(range(0,64))

    #     # print(index_scramble)

    #     random.shuffle(index_scramble)

    #     # print(index_scramble)

    #     # fill the chromosome with pieces at shuffled locations, with possible rotations
    #     for piece in seed:
    #         i = index_scramble.pop()
    #         # print("insert in spot ", i)
    #         # piece.show_piece()

    #         if random.random() < 0.05:
    #             # print("turned")
    #             # piece.show_piece()
    #             turned_piece = piece
    #             turned_piece.turn(random.randint(-3, 3))
    #             self.chromosome[i] = turned_piece
    #             # turned_piece.show_piece()
    #         else:
    #             self.chromosome[i] = piece

    def show_solution(self):
        print("solution: ")
        
        x = 0

        for piece in self.chromosome:
            if piece == None:
                print("none piece")
            else:
                print("spot: ", x)
                piece.show_piece()
                x += 1

            # if piece != None:
            #     print(piece.top, piece.right, piece.down, piece.left)

    def fitness(self):
        sum_row = 0
        sum_col = 0

        # x = 0

        # for piece in self.chromosome:
        #     print("spot: ", x)
        #     piece.show_piece()
        #     x += 1

        # count column and row mismatch, make this better ?
        for i in range(len(self.chromosome)):
            # print(i)
            # skip every 8th piece
            if (i+1) % 8 != 0:
                if self.chromosome[i].right != self.chromosome[i+1].left:
                    sum_row += 1

            # skip last row
            if i < 55:
                if self.chromosome[i].down != self.chromosome[i+8].top:
                    sum_col += 1

        self.row_mismatch = sum_row
        self.col_mismatch = sum_col
        self.score = sum_row + sum_col

        print("row mismatch: ", sum_row)
        print("column mismatch: ", sum_col)

    def crossover(self, other_solution):
        # need to implement crossover for permutations
        pass

        # children = []
        # return children

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
            s = Solution(seed)
            self.population.append(s)
        
        self.top_solution = self.population[0]

        # for solution in self.population:
        #     solution.show_solution()
    
    def order_population(self):
        self.population = sorted(self.population, key=lambda population: population.score)
        
    def compute_top(self, solution):
        if solution.score < self.top_solution.score:
            self.top_solution = solution

    def overall_score(self):
        sum = 0
        for solution in self.population:
            sum += solution.score
        return sum
    
    def select_parent(self, overall_score):
        parent = -1

        ran = random.random() * overall_score

        sum = 0
        i = 0
        while i < len(self.population) and sum < ran:
            sum += self.population[i].score
            parent += 1
            i += 1
        
        return parent

    def display(self):
        print("generation: ", self.population[0].generation)
        print("top (lowest) score: ", self.population[0].score)
        print("overall score: ", self.overall_score())
        self.population[0].show_solution()

    # solve
    def evolve(self, mutation_rate, num_gens, seed):
        self.initialize_population(seed)

        for solution in self.population:
            solution.fitness()

        self.order_population()

        self.top_solution = self.population[0]
        self.solution_track.append(self.top_solution.score)

        self.display()

        # iterate to evolve
        # for generation in range(num_gens):
        #     sum = self.overall_score()

        #     new_population = []

        #     for new_solutions in range(0, self.population_size, 2):
        #         parent1 = self.select_parent(sum)
        #         parent2 = self.select_parent(sum)

        #         children = self.population[parent1].crossover(self.population[parent2])

        #         new_population.append(children[0].mutation(mutation_rate))
        #         new_population.append(children[1].mutation(mutation_rate))

        #     self.population = list(new_population)

        #     for solution in self.population:
        #         solution.fitness()

        #     self.order_population()

        #     self.top_solution = self.population[0]
        #     self.solution_track.append(self.top_solution.score)
        #     self.compute_top()

        print("top solution score: ", self.top_solution.score)

        # for loop iterations

        return self.top_solution

        

# main
finput = open("Ass1Input.txt", "r")
seed = []
for i in range(0, 64):
    seed.append(Piece(i, finput.read(1), finput.read(1), finput.read(1), finput.read(1)))
    finput.read(1)

for piece in seed:
    piece.show_piece()


population_size = int(input("enter population size: "))
number_generations = int(input("enter number of generations: "))
mutation_rate = int(input("enter mutation rate (0-100): "))/100

GA = Genetic_algorithm(population_size)

solution_found = GA.evolve(mutation_rate, number_generations, seed)

