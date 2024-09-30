import random
import numpy as np

instruction_num_args = {
    -1: 3,
    -2: 1,
    -3: 1,
    -4: 0,
    -5: 3,
    -6: 2,
    -7: 2,
    -8: 1,
    -9: 1,
    -10: 3,
    -11: 3,
    # -12: 3,
    # -13: 1,
}

def generate_random_program():

    # pick a number of instructions to write
    num_instr_to_write = 10*3 # *3 to account for arguments
    range_to_pick_from = (-13,10)

    program = []

    for i in range(num_instr_to_write):
        program.append(random.randint(*range_to_pick_from))

    return program

def weighted_program_generation(instruction_weights=None, max_num_instructions=12):
    
    if not instruction_weights:
        instruction_weights = [1.0/len(instruction_num_args) for _ in range(len(instruction_num_args))]


    instruction_indices = list(range(-1,-12,-1))

    program = []

    for i in range(max_num_instructions):
        # choose an instruction
        instruction = np.random.choice(a=instruction_indices, p=instruction_weights)

        program.append(instruction)

        instruct_arg_ranges = [] # p = program tape, w = working tape, b = both working and program, i = input
        match instruction:
            case -1:
                instruct_arg_ranges = ['w', 'w', 'p']
            case -2:
                instruct_arg_ranges = ['w']
            case -3:
                instruct_arg_ranges = ['p']
            case -4:
                instruct_arg_ranges = []
            case -5:
                instruct_arg_ranges = ['w', 'w', 'p']
            case -6:
                instruct_arg_ranges = ['i', 'w']
            case -7:   
                instruct_arg_ranges = ['w', 'w']
            case -8:
                instruct_arg_ranges = ['b']
            case -9:
                instruct_arg_ranges = ['b']
            case -10:
                instruct_arg_ranges = ['w', 'w', 'w']
            case -11:
                instruct_arg_ranges = ['w', 'w', 'w']
            case _:
                raise NotImplementedError()
                

        # Add args
        for fill in instruct_arg_ranges:
            if fill == 'w':
                program.append(int(np.random.uniform(0,6)))
            elif fill == 'p':
                program.append(int(np.random.uniform(-12,0)))
            elif fill == 'b':
                program.append(int(np.random.uniform(1-max_num_instructions,6)))
            elif fill == 'i':
                program.append(0)

    return program