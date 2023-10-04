# include libraries
import random
import copy

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
            # print("no turn")
            pass
        if n == 1 or n == -3:
            # print("turn 1 or -3")
            self.top = left
            self.right = top
            self.down = right
            self.left = down
        if n == 2 or n == -2:
            # print("turn 2 or -2")
            self.top = down
            self.right = left
            self.down = top
            self.left = right
        if n == 3 or n == -1:
            # print("turn 3 or -1")
            self.top = right
            self.right = down
            self.down = left
            self.left = top

    def show_piece(self):
        print("piece ", self.id, ": ", self.top, self.right, self.down, self.left)
            

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
        # shuffle index 0-63
        # index_scramble = list(range(0,64))

        # # print(index_scramble)

        # random.shuffle(index_scramble)

        # # print(index_scramble)

        # # fill the chromosome with pieces at shuffled locations, with possible rotations
        # for piece in seed:
        #     i = index_scramble.pop()
        #     # print("insert in spot ", i)
        #     # piece.show_piece()

        #     if random.random() < 0.05:
        #         # print("turned")
        #         # piece.show_piece()
        #         turned_piece = piece
        #         turned_piece.turn(random.randint(-3, 3))
        #         self.chromosome[i] = turned_piece
        #         # turned_piece.show_piece()
        #     else:
        #         self.chromosome[i] = piece

        # for piece in self.chromosome:
        #     if piece == None:
        #         print("none piece")
        #     else:
        #         piece.show_piece()

    def randomize(self):
        # doesnt work for some reason
        # shuffle index 0-63
        # index_scramble = list(range(0,64))

        # print(index_scramble)

        # random.shuffle(index_scramble)

        # print(index_scramble)

        # temp = self.chromosome

        random.shuffle(self.chromosome)

        # fill the chromosome with pieces at shuffled locations, with possible rotations
        for piece in self.chromosome:
            # i = index_scramble.pop()
            # print("insert in spot ", i)
            # piece.show_piece()

            if random.random() < 0.05:
                # print("turned")
                # piece.show_piece()
                # turned_piece = piece
                # turned_piece.turn(random.randint(-3, 3))
                # self.chromosome[i] = turned_piece
                # turned_piece.show_piece()

                # print("turning")
                # piece.show_piece()

                piece.turn(random.randint(-3, 3))
                
                # piece.show_piece()

            # else:
            #     self.chromosome[i] = piece
        
        # self.show_solution()

    def show_solution(self):
        print("\nsolution: ")
        
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
        
        print("score: ", self.score)

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

        # print("row mismatch: ", sum_row)
        # print("column mismatch: ", sum_col)

    def crossover(self, other_solution, seed):
        # can also implement pmx, cycle, edge recomb

        # print("parents: ")
        # self.show_solution()
        # other_solution.show_solution()

        child1 = copy.deepcopy(self)
        child1.generation = self.generation + 1

        child2 = copy.deepcopy(other_solution)
        child2.generation = self.generation + 1

        crossover1 = random.randint(0, len(self.chromosome)-2)
        crossover2 = random.randint(crossover1+1, len(self.chromosome)-1)

        # print("crossovers: ", crossover1, crossover2)

        segment1 = self.chromosome[crossover1:crossover2]
        segment2 = other_solution.chromosome[crossover1:crossover2]

        used_ids1 = set()
        used_ids2 = set()

        for i in range(len(segment1)):
            used_ids1.add(segment1[i].id)
            used_ids2.add(segment2[i].id)
            
        # print("segment1 piece ids: ", used_ids1)
        # print("segment2 piece ids: ", used_ids2)

        index1 = crossover2
        index2 = crossover2

        # print("crossover after segment: ", crossover2)

        for i in range(crossover2, len(self.chromosome)):
            # print("sol index: ", i)
            while other_solution.chromosome[index1].id in used_ids1:
                # print("index1: ", index1)
                index1 = (index1+1) % 64
            # print("selected index1: ", index1)
            child1.chromosome[i] = other_solution.chromosome[index1]
            index1 = (index1+1) % 64

            while self.chromosome[index2].id in used_ids2:
                # print("index2: ", index2)
                index2 = (index2+1) % 64
            # print("selected index2: ", index2)
            child2.chromosome[i] = self.chromosome[index2]
            index2 = (index2+1) % 64

        for i in range(crossover1):
            # print("sol index: ", i)
            while other_solution.chromosome[index1].id in used_ids1:
                # print("index1: ", index1)
                index1 = (index1+1) % 64
            # print("selected index1: ", index1)
            child1.chromosome[i] = other_solution.chromosome[index1]
            index1 = (index1+1) % 64

            while self.chromosome[index2].id in used_ids2:
                # print("index2: ", index2)
                index2 = (index2+1) % 64
            # print("selected index2: ", index2)
            child2.chromosome[i] = self.chromosome[index2]
            index2 = (index2+1) % 64

        # print("parents:")
        # self.show_solution()
        # other_solution.show_solution()

        # print("children:")
        # child1.show_solution()
        # child2.show_solution()

        return [child1, child2]

    def mutation(self, rate):
        # can also implement swap, insert, scramble, inversion
        for i in range(len(self.chromosome)):
            if random.random() < rate: 
                # print("turning piece: ", i)
                self.chromosome[i].turn(random.randint(-3, 3))
        

class Genetic_algorithm():
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []
        self.generation = 0
        self.top_solution = None
        self.solution_track = []

    def initialize_population(self, seed):
        initial_solution = Solution(seed)


        for i in range(self.population_size):
            sol = copy.deepcopy(initial_solution)
            sol.randomize()
            self.population.append(sol)
        
        self.top_solution = self.population[0]

        # print("first population:")
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
        # self.population[0].show_solution()

    # solve
    def evolve(self, mutation_rate, num_gens, seed):
        print("\n\n================= init population =================")
        self.initialize_population(seed)

        for solution in self.population:
            # solution.show_solution()
            solution.fitness()

        # print("\n\n================= order population =================")
        self.order_population()

        self.top_solution = self.population[0]
        self.solution_track.append(self.top_solution.score)

        self.display()

        print("\n\n================= start evolving =================")

        # iterate to evolve
        for generation in range(num_gens):
            # print("\n\n================= ordered population =================")
            # for solution in self.population:
            #     solution.show_solution()

            sum = self.overall_score()

            new_population = []

            for new_solutions in range(0, self.population_size, 2):
                parent1 = self.select_parent(sum)
                parent2 = self.select_parent(sum)

                children = self.population[parent1].crossover(self.population[parent2], seed)

                # print("\nparents: ", parent1, parent2)

                # print("\nchildren:")
                # children[0].show_solution()
                # children[1].show_solution()

                child1 = copy.deepcopy(children[0])
                child2 = copy.deepcopy(children[1])

                child1.mutation(mutation_rate)
                child2.mutation(mutation_rate)

                new_population.append(child1)
                new_population.append(child2)

            print("\n\n================= new generation =================")
            # for solution in new_population:
            #     solution.show_solution()

            self.population = new_population

            for solution in self.population:
                # solution.show_solution()
                solution.fitness()

            # print("\n\n================= order population =================")
            self.order_population()

            self.display()
            self.solution_track.append(self.population[0].score)
            self.compute_top(self.population[0])

        print("top solution score: ", self.top_solution.score)


        return self.top_solution

        

# # main
finput = open("Ass1Input.txt", "r")
seed = []
for i in range(0, 64):
    seed.append(Piece(i, finput.read(1), finput.read(1), finput.read(1), finput.read(1)))
    finput.read(1)
finput.close()
# for piece in seed:
#     piece.show_piece()



# sol = Solution(seed)

# s1 = copy.deepcopy(sol)
# print("solution 1:")
# s1.randomize()
# s1.show_solution()

# s2 = copy.deepcopy(sol)
# print("solution 2:")
# s2.randomize()
# s2.show_solution()

# children = s1.crossover(s2, seed)

# print("child 1:")
# children[0].show_solution()

# print("child 2:")
# children[1].show_solution()

# sols = []

# initial_solution = Solution(seed)

# # Create copies of the initial solution and append them to sols
# for i in range(3):
#     sol = copy.deepcopy(initial_solution)
#     sols.append(sol)

# for i in range(0,3):
#     print("\n\nbefore randomize:")
#     sols[i].show_solution()
#     sols[i].randomize()
#     print("\nafter randomize:")
#     sols[i].show_solution()





population_size = int(input("enter population size: "))
number_generations = int(input("enter number of generations: "))
mutation_rate = int(input("enter mutation rate (0-100): "))/100

GA = Genetic_algorithm(population_size)

solution_found = GA.evolve(mutation_rate, number_generations, seed)

foutput = open("Ass1Output.txt", "w")

solution_str = "Mihai Olaru 40111734 Amir Cherif 40047635\n"
for i in range(len(solution_found.chromosome)):
    piece = str(solution_found.chromosome[i].top) + str(solution_found.chromosome[i].right) + str(solution_found.chromosome[i].down) + str(solution_found.chromosome[i].left)
    
    # print("piece: ", solution_found.chromosome[i].id)

    if i == 63:
        break

    if (i + 1) % 8 == 0:
        solution_str += piece + "\n"
    else:
        solution_str += piece + " "

solution_str += piece

# print(solution_str)

foutput.write(solution_str)
foutput.close()