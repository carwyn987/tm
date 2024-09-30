import random
from deap import base
from deap import creator
from deap import tools

from tm.program_generators.generator import weighted_program_generation as wpg
from tm.dataset_generators.generators import generate_ones, generate_indxs
from tm.losses.mse import index_match_MSE, MSE, binary
from tm.tm import TM

def test_ga_tm():
    inputs = []
    labels = generate_indxs(100)

    # Define the chromosome structure
    IND_SIZE = 36

    # Create the fitness class and individual class
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    # Create the toolbox
    toolbox = base.Toolbox()

    # Use your weighted_program_generation function to generate the initial population
    def weighted_program_generation():
        generated = wpg()
        other = IND_SIZE - len(generated)
        individual = creator.Individual(generated + [-4]*other)
        return individual

    toolbox.register("individual", weighted_program_generation)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Define the evaluation function (you'll need to implement this)
    def evaluate(individual):
        
        fitness_fn = binary
        max_steps = 1000
        
        # Set up turing machine
        tm = TM()
        tm.setup_program(individual)
        tm.setup_inputs(inputs)

        # Set up executor
        fitness, response, steps = tm.run(max_steps, fitness_fn, labels)
        return fitness,

    # Register the evaluation function with the toolbox
    toolbox.register("evaluate", evaluate)

    # Register the crossover, mutation, and selection functions with the toolbox
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=-11, up=6, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Run the genetic algorithm
    def run_genetic_algorithm():
        pop = toolbox.population(n=50)
        CXPB, MUTPB, NGEN = 0.5, 0.4, 5000

        # Evaluate the initial population
        fitnesses = map(toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for g in range(NGEN):
            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

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
            best_ind = min(pop, key=lambda ind: ind.fitness.values[0])
            print(f"Generation {g}: Best fitness = {best_ind.fitness.values[0]}")

        print("Best individual:", best_ind)

    # Run the genetic algorithm
    run_genetic_algorithm()