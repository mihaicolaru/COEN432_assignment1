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

    # turn by how much (+clockwise, -counter)
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

    # shuffle chromosome
    def randomize(self):
        random.shuffle(self.chromosome)

        # fill the chromosome with pieces at shuffled locations, with possible rotations (maybe make dependant on mutation rate?)
        for piece in self.chromosome:
            if random.random() < 0.05:
                piece.turn(random.randint(-3, 3))                
                # piece.show_piece()
        # self.show_solution()

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

    def fitness(self):
        sum_row = 0
        sum_col = 0

        # count column and row mismatch, TODO: make this better ?
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
        # print("row mismatch: ", sum_row)
        # print("column mismatch: ", sum_col)
        self.score = sum_row + sum_col        

    # ordered crossover implementation
    def crossover(self, other_solution, cross_rate):
        #TODO: can also implement pmx, cycle, edge recomb

        if random.random() < cross_rate:  # this is where you set the rate of crossover
            # print("parents: ")
            # self.show_solution()
            # other_solution.show_solution()

            # create copy of parents (to avoid modifying them)
            child1 = copy.deepcopy(self)
            child1.generation = self.generation + 1

            child2 = copy.deepcopy(other_solution)
            child2.generation = self.generation + 1

            # pick 2 crossover points in the chromosome
            crossover1 = random.randint(0, len(self.chromosome)-2)
            crossover2 = random.randint(crossover1+1, len(self.chromosome)-1)
            # print("crossovers: ", crossover1, crossover2)

            # isolate the segment from the parents
            segment1 = self.chromosome[crossover1:crossover2]
            segment2 = other_solution.chromosome[crossover1:crossover2]

            used_ids1 = set()
            used_ids2 = set()

            # identify the used pieces in each segment
            for i in range(len(segment1)):
                used_ids1.add(segment1[i].id)
                used_ids2.add(segment2[i].id)            
            # print("segment1 piece ids: ", used_ids1)
            # print("segment2 piece ids: ", used_ids2)

            # fill in children chromosome with opposing parent pieces, skipping over pieces already in respective segment
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

            # check child fitness
            child1.fitness()
            child2.fitness()

            # create new generation copy of parents (could maybe just update generation?)
            new_parent1 = copy.deepcopy(self)
            new_parent1.generation +=1

            new_parent2 = copy.deepcopy(other_solution)
            new_parent2.generation +=1

            candidates = [new_parent1, new_parent2, child1, child2]
            # print("\n\ncandidate solutions (p1, p2, c1, c2)")
            # for solution in candidates:            
            #     solution.show_solution()

            candidates = sorted(candidates, key=lambda candidates: candidates.score)

            # pick best 2 out of children and parents
            children = candidates[0:2]
            # print("\n\npicked solutions")
            # for solution in children:
            #     solution.show_solution()
        else:
            new_parent1 = copy.deepcopy(self)
            new_parent1.generation +=1

            new_parent2 = copy.deepcopy(other_solution)
            new_parent2.generation +=1
            children = [new_parent1, new_parent2]

        return children

    def mutation(self, rate):
        #TODO: can also implement swap, insert, scramble, inversion
        for i in range(len(self.chromosome)):
            if random.random() < rate: 
                # print("turning piece: ", i)
                self.chromosome[i].turn(random.randint(-3, 3))
        
class Genetic_algorithm():
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []
        # self.generation = 0
        self.top_solution = None
        self.solution_track = []

    def initialize_population(self, seed):
        initial_solution = Solution(seed)

        # create copy of initial solution (otherwise they all get modified in the same way)
        for i in range(self.population_size):
            sol = copy.deepcopy(initial_solution)
            sol.randomize()
            self.population.append(sol)
        
        # save current best solution (random)
        self.top_solution = self.population[0]
        # print("first population:")
        # for solution in self.population:
        #     solution.show_solution()
    
    def order_population(self):
        self.population = sorted(self.population, key=lambda population: population.score)
        
    # update top solution if a better one is found
    def compute_top(self, solution):
        if solution.score < self.top_solution.score:
            self.top_solution = solution

    # computes generation total score (can also implement median perhaps?)
    def overall_score(self):
        sum = 0
        for solution in self.population:
            sum += solution.score
        return sum
    
    def select_parent(self, overall_score):
        #TODO: can try fitness proportionate, rank based, linear, exponential, tournament, uniform
        parent = -1

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
        print("generation: ", self.population[0].generation)
        print("generation top (lowest) score: ", self.population[0].score)
        print("current top (lowest) score: ", self.top_solution.score, self.top_solution.generation)
        print("overall score: ", self.overall_score())
        # self.population[0].show_solution()

    # solve
    def evolve(self, mutation_rate, cross_rate, num_gens, seed):
        print("\n\n================= init population =================")
        self.initialize_population(seed)

        for solution in self.population:
            # solution.show_solution()
            solution.fitness()

        self.order_population()

        self.top_solution = self.population[0]
        self.solution_track.append(self.top_solution.score)

        self.display()

        print("\n\n================= start evolving =================")

        # iterate to evolve
        for generation in range(num_gens):
            # for solution in self.population:
            #     solution.show_solution()

            sum = self.overall_score()

            new_population = []

            if generation % (num_gens/10) == 0:                
                mutation_rate *= 1.02
                cross_rate /= 1.02

                print("#######################################################################################")

                print("new mutation", mutation_rate*100,"\ncrossover: ", cross_rate*100)

                print("#######################################################################################")

            for new_solutions in range(0, self.population_size, 2):
                parent1 = self.select_parent(sum)
                parent2 = self.select_parent(sum)

                children = self.population[parent1].crossover(self.population[parent2], cross_rate)

                #TODO: could try saving all parents + children for tournament survivor selection, or generation more children than parents, etc

                # print("\nparents: ", parent1, parent2)

                # print("\nchildren:")
                # children[0].show_solution()
                # children[1].show_solution()

                child1 = children[0] #copy.deepcopy(children[0])
                child2 = children[1] #copy.deepcopy(children[1])

                #TODO: perhaps check if mutation goes in the right direciton, or have mutation rate change
                child1.mutation(mutation_rate)
                child2.mutation(mutation_rate)

                new_population.append(child1)
                new_population.append(child2)

            print("\n\n================= new generation =================") 
            # for solution in new_population:
            #     # solution.show_solution()
            #     solution.fitness()

            # new_sum = 0
            # for solution in new_population:
            #     new_sum += solution.score

            # if new_sum < sum:
            #     print("picked new pop")
            #     self.population = new_population
            #     self.order_population()
            #     self.compute_top(self.population[0])
            # else:
            #     print("picked old pop")
            #     for solution in self.population:
            #         solution.generation = self.population[0].generation + 1

            self.population = new_population

            for solution in self.population:
                # solution.show_solution()
                solution.fitness()

            self.order_population()

            self.compute_top(self.population[0])                
            
            self.solution_track.append(self.population[0].score)

            self.display()

            # self.generation += 1            

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

# get parameters from the user (perhaps remove mutation when we automate it)
population_size = int(input("enter population size: "))
number_generations = int(input("enter number of generations: "))
# mutation_rate = float(input("enter mutation rate (0-100): "))/100
# cross_rate = float(input("enter crossover rate (0-100): "))/100
mutation_rate = float(0.1)/100
cross_rate = float(100)/100


GA = Genetic_algorithm(population_size)

solution_found = GA.evolve(mutation_rate, cross_rate, number_generations, seed)

solution_found.show_solution()

# write solution to file
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