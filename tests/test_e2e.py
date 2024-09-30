import random
import copy
from tqdm import tqdm
import numpy as np

from tm.dataset_generators.generators import generate_ones, generate_indxs
from tm.losses.mse import index_match_MSE, MSE, binary
from tm.tm import TM
from tm.program_generators.generator import generate_random_program, weighted_program_generation

def test_e2e():
    
    # Set up data for ones test
    inputs = []
    labels = generate_indxs(100)

    fitness_fn = binary
    stopping_cond = 30000000
    max_steps = 1000

    min_fitness =  np.inf        
    count = 0
    for i in tqdm(range(stopping_cond)):
        count += 1

        # Generate a random program
        program = weighted_program_generation() # generate_random_program()
        save_program = program

        # Set up turing machine
        tm = TM()
        tm.setup_program(program)
        tm.setup_inputs(inputs)

        # Set up executor
        fitness, response, steps = tm.run(max_steps, fitness_fn, labels)

        if fitness < min_fitness:
            min_fitness = fitness

            tm.setup_program(save_program)
            print("\n", "Output: ", tm.output_tape, "\nLabels: ", labels[0:10], "...")
            print("TM tapes: ", tm.program_working_tape.verbose())
            print("Fitness: ", fitness)

        if fitness == 0:
            return
    
    assert False
