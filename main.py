import numpy as np
import sys
from random import uniform, randint
from sys import exit


# Initially generate the population
def generatePop(num_pop):
    pop_list = []
    for i in range(0, num_pop):
        elem = randint(0, 255)
        pop_list.append(elem / 256)
    return pop_list


# Encode a float in (0,1). Return a binary string
def encode(num):
    assert (num>=0 and num<1), "Input must be in range [0,1)"
    int_num = int(num * 256)
    return '{:08b}'.format(int_num)


# Decode a binary string representation into float
def decode (bin_str):
    assert len(bin_str) == 8, "Binary string must be represented by 8 bits"
    int_num = int(bin_str, 2)
    return int_num / 256


# f(x) function
def f(x):
      return x*x +4*x + 5


# Fitness function
# We want to find f(x) as small as possible, so fitness = 1 / f(x) should be as big as possible
def fitness(x):
    return 1 / f(x)


# Choose num_mem members of the population based on Russian Roullete
# Input: List of floats, number of outputs
# Output: List of num_mem (num of members) of floats
def roulette(pop_list, num_mem):
    # Calculate sum of fitness of population
    fit_sum = 0
    for chromo in pop_list:
        fit_sum += fitness(chromo)

    # Generate a probality list
    prob_list = []
    prob_sum = 0
    for chromo in pop_list:
        prob = (fitness(chromo) / fit_sum)
        prob_sum += prob
        prob_list.append(prob_sum)

    # Choose parents
    chosen = []
    for i_mem in range(0,num_mem):
        seed = uniform(0, 1) # Random number between 0 and 1
        if seed < prob_list[0]:
            chosen.append(pop_list[0])
        elif seed >= prob_list[-1]:
            chosen.append(pop_list[-1])
        else:
            for i in range(0, len(pop_list)-1):
                if (seed >= prob_list[i]) and (seed < prob_list[i+1]):
                    chosen.append(pop_list[i])
                    break
            
    assert len(chosen) == num_mem
    return chosen


# Crossover function on a chosen position.
# Input: List of 2 floats.
# Return: List of 2 floats.
def crossover(parents, pos):
    parent1 = encode(parents[0])
    parent2 = encode(parents[1])

    child1 = parent1[:pos] + parent2[pos:]
    child2 = parent2[:pos] + parent1[pos:]

    child1 = decode(child1)
    child2 = decode(child2)

    return [child1, child2]


# Randomly mutate children after mating: Change one bit randomly
# Input: Float
# Output: Altered binary string
def mutate(child):
    chrom = encode(child)
    pos = randint(0, 7)
    l = list(chrom)
    if l[pos] == '0':
        l[pos] = '1'
    elif l[pos] == '1':
        l[pos] = '0'
    return decode("".join(l))


# Main function
if __name__ == "__main__":

    # Generate parameters and population
    num_pop = 100 # Population 100
    crossover_rate = 0.3 # % of the population will participate in crossver
    mutation_rate = 0.01 # % of mutation chance
    pos_crossover = randint(1,7) # Position to cut the chromosome to do crossover
    num_iter = 100 # Number of iterations
    pop_list = generatePop(num_pop)


    # Loop
    for i in range(0, num_iter):

        # Choose parents from the population and crossover
        nb_parent_pairs = int((num_pop * crossover_rate) / 2)
        for i in range(0, nb_parent_pairs):
            parents = roulette(pop_list, 2)
            childs_crossover = crossover(parents, pos_crossover)

            # Mutation and add child to the population
            for child in childs_crossover:
                seed_mutation = uniform(0, 1)
                if seed_mutation <= mutation_rate:
                    child_mutated = mutate(child)
                    pop_list.append(child_mutated)
                else:
                    pop_list.append(child)
            
        # Choose n chromos to the next population
        pop_list = roulette(pop_list, num_pop)



# Show the "fittest" chromo
fit_list = []
for elem in pop_list:
    fit_list.append(fitness(elem))

print("Min value by genetic algorithm:\n{}".format(min(fit_list)))
print("\nOptimal min value:\n{}".format(fitness(1)))