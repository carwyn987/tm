from deap import base, creator, tools, algorithms
import numpy as np
import random
import matplotlib.pyplot as plt


def track_progress(pop, gen):
    # Get the best individual from the current population
    best_ind = max(pop, key=lambda ind: ind.fitness.values[0])
    
    # Print the best individual's fitness at each generation
    print(f"Generation {gen}: Best fitness = {best_ind.fitness.values[0]}")
    
    return best_ind.fitness.values[0]

def test_ga():

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    IND_SIZE = 10

    toolbox = base.Toolbox()
    toolbox.register("attribute", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                    toolbox.attribute, n=IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        return sum(individual),

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    pop = toolbox.population(n=50)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Initialize a list to store the best fitness at each generation
    best_fitness_over_gens = []

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        # offspring = map(toolbox.clone, offspring)
        offspring = [toolbox.clone(ind) for ind in toolbox.select(pop, len(pop))]

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Track the progress
        best_fitness = track_progress(pop, g)
        best_fitness_over_gens.append(best_fitness)

    # Plot the best fitness over generations
    plt.plot(best_fitness_over_gens)
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Genetic Algorithm Progress")
    plt.show()
