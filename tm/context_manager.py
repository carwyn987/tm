import copy
import random
from tqdm import tqdm


from levin_tm_module.tm import TM
from levin_tm_module.executor import Executor

from levin_tm_module.program_generators.generator import generate_random_program

class ContextManager:
    """
    Context Manager (CM) defines an init program, program update algorithm (random, GA), success conditions
    CM should then repeatedly call executor for the program, compute fitness (with test data), and decide to continue or stop
    Arguments:
    ----------
     - Inputs (entire dataset)
     - Labels (entire dataset)
     - Initial Program
     - Program Update Algorithm
     - Fitness Function
     - Stopping Condition (# programs tested or appropriate fitness)
     - max_steps (int): Number of steps to run a program for before stopping.

    Returns:
    --------
     - best program
     - fitness
     - status
    """
    def __init__(self, inputs, labels, fitness_fn, stopping_cond, max_steps):

        self.inputs = inputs
        self.labels = labels
        self.fitness_fn = fitness_fn
        self.stopping_cond = stopping_cond
        self.max_steps = max_steps

        # Split data into train and test
        label_indxs = list(range(0,len(labels)))
        matching_format = list(zip(label_indxs,labels))

        # Sample labels
        self.train_input = []
        self.train_matching_format = matching_format[0:5] # random.sample(matching_format, 3)

        self.best_tms = []

        print("Training Data: ", self.train_matching_format)


    def run(self):

        pbar = tqdm(total=self.stopping_cond)
        
        # In a loop, set up a TM, set up an executor, run the executor, and track final fitnesses
        # best_fitness = 1e10
        count = 0
        while True:
            count += 1

            # Generate a random program
            program = generate_random_program()

            # Set up turing machine
            tm = TM()
            tm.setup_program(program)
            tm.setup_inputs(self.inputs)

            # Set up executor
            executor = Executor(tm, max_steps=self.max_steps, labels=self.train_matching_format, fitness_fn=self.fitness_fn)

            fitness, response, steps = executor.run()

            # print("Program workign tape: ", tm.program_working_tape)
            # print("input tape: ", tm.input_tape)
            # print("labels:     ", self.labels)

            if fitness == 0:
                self.best_tms.append((count, copy.deepcopy(tm), fitness, response, steps))
                # TEMPORARY
                # return self.best_tms

            # Stopping conditions
            if count >= self.stopping_cond and len(self.best_tms) > 0:
                return self.best_tms
            elif count >= self.stopping_cond:
                return None

            pbar.update(1)