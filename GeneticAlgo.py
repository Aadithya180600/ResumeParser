# Program to implement Genetic Algorithm
# Implemented by Considering this as a 0 1 Knapsack problem

__author__ = "Sai Sangameswara Aadithya Kanduri"


import random
from ResumeParser import ResumeParser

# function to generate a random population


class GeneticAlgo:

    def __init__(self, items, resumeSkills, requiredSkills) -> None:
        self.items = items
        self.resumeSkills = resumeSkills
        self.resumeParser = ResumeParser()
        self.threshold = 0.75  # Declared manually for testing
        self.required_skills = requiredSkills
        self.eligibility_probability = 0
    
    # Method for Constructing Eligibility Probability
    def CalEligibilityProbability(self, applicantSkills):
        
        if(len(applicantSkills) == 0):
            applicantSkills = self.resumeSkills
        count_skills = 0
        for i in applicantSkills:
            if i in self.required_skills:   
                count_skills += 1

        self.eligibility_probability = count_skills/len(self.required_skills)

    # Method to say is eligible or not
    def isEligible(self):
        if self.threshold <= self.eligibility_probability:
            return True
        return False

    def generate_population(self, size):
        """
        Method to generate and initialise the population
        """
        population = []
        for _ in range(size):
            genes = [0, 1]
            chromosome = []
            for _ in range(len(self.items)):
                chromosome.append(random.choice(genes))
            population.append(chromosome)
        # print(population)
        return population

    # function to calculate the fitness of a chromosome

    def calculate_fitness(self, chromosome):
        """
        Method to calculate the fitness
        """
        total_weight = 0
        total_value = 0
        skills = self.resumeSkills[:]
        # print(skills)
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                total_weight += self.items[i][1]
                total_value += self.items[i][2]
                skills.append(self.items[i][0])
                self.CalEligibilityProbability(skills)
        
        if self.isEligible():
            if total_value>0:
                return total_value
            return 10000
        else:
            return 10000

    def select_chromosomes(self, population):
        """
        Method to select two chromosomes for crossover
        """
        fitness_values = []
        for chromosome in population:
            fitness_values.append(self.calculate_fitness(chromosome))

        fitness_values = [float(i)/sum(fitness_values) for i in fitness_values]

        parent1 = random.choices(population, weights=fitness_values, k=1)[0]
        parent2 = random.choices(population, weights=fitness_values, k=1)[0]

        # print("Selected two chromosomes for crossover")
        return parent1, parent2

    def crossover(self, parent1, parent2):
        """
        function to perform crossover between two chromosomes
        """
        crossover_point = random.randint(0, len(self.items)-1)
        child1 = parent1[0:crossover_point] + parent2[crossover_point:]
        child2 = parent2[0:crossover_point] + parent1[crossover_point:]

        # print("Performed crossover between two chromosomes")
        return child1, child2

    def mutate(self, chromosome):
        """
        Method to perform mutation on a chromosome
        """
        mutation_point = random.randint(0, len(self.items)-1)
        # print(mutation_point)
        if chromosome[mutation_point] == 0:
            chromosome[mutation_point] = 1
        else:
            chromosome[mutation_point] = 0
        # print("Performed mutation on a chromosome")
        return chromosome

    def get_best(self, population):
        """
        Method to get the best chromosome from the population
        """
        fitness_values = []
        for chromosome in population:
            fitness_values.append(self.calculate_fitness(chromosome))
        max_value = min(fitness_values)
        max_index = fitness_values.index(max_value)
        return population[max_index]

    def geneticAlgo(self) -> list:
        population_size = 10
        mutation_probability = 0.2
        generations = 100

        # generate a random population
        population = self.generate_population(population_size)
        parent1 = ''
        parent2 = ''
        # evolve the population for specified number of generations
        for _ in range(generations):
            # select two chromosomes for crossover
            try:
                parent1, parent2 = self.select_chromosomes(population)
            except ZeroDivisionError as e:
                # print("Error: Cannot divide by zero")
                pass

            # perform crossover to generate two new chromosomes
            child1, child2 = self.crossover(parent1, parent2)

            # perform mutation on the two new chromosomes
            if random.uniform(0, 1) < mutation_probability:
                child1 = self.mutate(child1)
            if random.uniform(0, 1) < mutation_probability:
                child2 = self.mutate(child2)

            # replace the old population with the new population
            population = [child1, child2] + population[2:]

        # get the best chromosome from the population
        best = self.get_best(population)

        suggestedSkills = []
        for i in best:
            if i == 1:
                suggestedSkills.append(self.items[i][0])
        return suggestedSkills
