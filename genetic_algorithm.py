from random import random
import matplotlib.pyplot as plt
import pymysql

class Product():
  def __init__(self, name, space, price):
    self.name = name
    self.space = space
    self.price = price

class Individual():
  def __init__(self, spaces, prices, space_limit, generation=0):
    self.spaces = spaces
    self.prices = prices
    self.space_limit = space_limit
    self.score_evaluation = 0
    self.used_space = 0
    self.generation = generation
    self.chromosome = []

    for i in range(len(spaces)):
      if random() < 0.5:
        self.chromosome.append('0')
      else:
        self.chromosome.append('1')

  def fitness(self):
    score = 0
    sum_spaces = 0
    for i in range(len(self.chromosome)):
      if self.chromosome[i] == '1':
        score += self.prices[i]
        sum_spaces += self.spaces[i]
    if sum_spaces > self.space_limit:
      score = 1
    self.score_evaluation = score
    self.used_space = sum_spaces

  def crossover(self, other_individual):
    cutoff = round(random() * len(self.chromosome))

    child1 = other_individual.chromosome[0:cutoff] + self.chromosome[cutoff::]
    child2 = self.chromosome[0:cutoff] + other_individual.chromosome[cutoff::]
    children = [Individual(self.spaces, self.prices, self.space_limit, self.generation + 1),
                Individual(self.spaces, self.prices, self.space_limit, self.generation + 1)]
    children[0].chromosome = child1
    children[1].chromosome = child2
    return children

  def mutation(self, rate):
    for i in range(len(self.chromosome)):
      if random() < rate:
        if self.chromosome[i] == '1':
          self.chromosome[i] = '0'
        else:
          self.chromosome[i] = '1'
    return self

class GeneticAlgorithm():
  def __init__(self, population_size):
    self.population_size = population_size
    self.population = []
    self.generation = 0
    self.best_solution = None
    self.list_of_solutions = []

  def initialize_population(self, spaces, prices, space_limit):
    for i in range(self.population_size):
      self.population.append(Individual(spaces, prices, space_limit))
    self.best_solution = self.population[0]

  def order_population(self):
    self.population = sorted(self.population, key=lambda population: population.score_evaluation, reverse=True)

  def best_individual(self, individual):
    if individual.score_evaluation > self.best_solution.score_evaluation:
      self.best_solution = individual

  def sum_evaluations(self):
    sum = 0
    for individual in self.population:
      sum += individual.score_evaluation
    return sum

  def select_parent(self, sum_evaluation):
    parent = -1
    random_value = random() * sum_evaluation
    sum = 0
    i = 0
    while i < len(self.population) and sum < random_value:
      sum += self.population[i].score_evaluation
      parent += 1
      i += 1
    return parent

  def visualize_generation(self):
    best = self.population[0]
    print('Generation: ', self.population[0].generation,
          'Total price: ', best.score_evaluation, 'Space: ', best.used_space,
          'Chromosome: ', best.chromosome)

  def solve(self, mutation_probability, number_of_generations, spaces, prices, limit):
    self.initialize_population(spaces, prices, limit)

    for individual in self.population:
      individual.fitness()
    self.order_population()
    self.best_solution = self.population[0]
    self.list_of_solutions.append(self.best_solution.score_evaluation)

    self.visualize_generation()

    for generation in range(number_of_generations):
      sum = self.sum_evaluations()
      new_population = []
      for new_individuals in range(0, self.population_size, 2):
        parent1 = self.select_parent(sum)
        parent2 = self.select_parent(sum)
        children = self.population[parent1].crossover(self.population[parent2])
        new_population.append(children[0].mutation(mutation_probability))
        new_population.append(children[1].mutation(mutation_probability))

      self.population = list(new_population)

      for individual in self.population:
        individual.fitness()
      self.visualize_generation()
      best = self.population[0]
      self.list_of_solutions.append(best.score_evaluation)
      self.best_individual(best)

    print('**** Best solution - Generation: ', self.best_solution.generation,
          'Total price: ', self.best_solution.score_evaluation, 'Space: ', self.best_solution.used_space,
          'Chromosome: ', self.best_solution.chromosome)

    return self.best_solution.chromosome

if __name__ == '__main__':
    products_list = []
    connection = pymysql.connect(host='localhost', user='root', passwd='12345678', db='products')
    cursor = connection.cursor()
    cursor.execute('select product_name, space, price, quantity from products')
    for product in cursor:
        #print(product[0], product[1], product[2])
        for i in range(product[3]):
            products_list.append(Product(product[0], product[1], product[2]))
    cursor.close()
    connection.close()

    #print(products_list)
    #for product in products_list:
    #    print(product.name)
    #print(len(products_list))

    spaces = []
    prices = []
    names = []
    for product in products_list:
        spaces.append(product.space)
        prices.append(product.price)
        names.append(product.name)
    limit = 10
    population_size = 20
    mutation_probability = 0.01
    number_of_generations = 100
    ga = GeneticAlgorithm(population_size)
    result = ga.solve(mutation_probability, number_of_generations, spaces, prices, limit)

    print('\n')
    for i in range(len(products_list)):
        if result[i] == '1':
            print('Name: ', products_list[i].name, ' - Price: ', products_list[i].price)

    plt.plot(ga.list_of_solutions)
    plt.title("Genetic algorithm results")
    plt.show()


















