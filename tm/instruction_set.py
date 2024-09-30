# def jumpleq(program_working_tape, program_ptr_idx):
#     # jumpleq(address1, address2, address3)
#     # If the contents of address1 is less than or equal to the contents of address2, the InstructionPointer is set equal to address3

#     if not program_working_tape[program_ptr_idx-1] <= program_working_tape[program_ptr_idx-2]:
#         move_forward = 4
#     elif program_working_tape[program_ptr_idx-3] is not None and program_working_tape[program_ptr_idx-3] < 0:
#         program_ptr_idx = program_working_tape[program_ptr_idx-3]
#         move_forward = 0 # CONDITIONAL
#     else:
#         raise IndexError()
    
#     return move_forward, program_ptr_idx

# instruction_set = {
#     "-1": {
#         "name": "jumpleq",
#         "inputs": "address1, address2, address3",
#         "input_length": 3,
#         "description": "If the contents of address1 is less than or equal to the contents of address2, the InstructionPointer is set equal to address 3",
#         "command": "if $address1 <= $address2: instruction_pointer = address3"
#     },
#     "-2": {
#         "name": "output",
#         "inputs": "address1",
#         "input_length": 1,
#         "description": "A primitive for interaction with the external environment. It corresponds to the TM action of 'writing the output tape'",
#         "command": "output_tape.append($address1)"
#     },
#     "-3": {
#         "name": "jump",
#         "inputs": "address1",
#         "input_length": 1,
#         "description": "The InstructionPointer is set equal to address1",
#         "command": "instruction_pointer = $address1"
#     },
#     "-4": {
#         "name": "stop",
#         "inputs": "",
#         "input_length": 0,
#         "description": "Halt the current program",
#         "command": "return 1"
#     },
#     "-5": {
#         "name": "add",
#         "inputs": "address1, address2, address3",
#         "input_length": 3,
#         "description": "The contents of address1 is added to the contents of address2, the result is written into address3",
#         "command": "$address3 = $address1 + $address2"
#     },
#     "-6": {
#         "name": "getInput",
#         "inputs": "address1, address2",
#         "input_length": 2,
#         "description": "Reads the current value of the ith input (value at address1) into address2",
#         "command": "$address2 = input_tape[$address1]"
#     },
#     "-7": {
#         "name": "move",
#         "inputs": "address1, address2",
#         "input_length": 2,
#         "description": "The contents of address1 is copied into address2",
#         "command": "$address2 = $address1"
#     },
#     "-8": {
#         "name": "allocate",
#         "inputs": "address1",
#         "input_length": 1,
#         "description": "The size of the working tape is increased by the value found in address1, initializing all cells to zero",
#         "command": "working_tape.extend([0] * $address1)"
#     },
#     "-9": {
#         "name": "Increment",
#         "inputs": "address1",
#         "input_length": 1,
#         "description": "The contents of address1 is incremented",
#         "command": "$address1 += 1"
#     },
#     "-10": {
#         "name": "Decrement",
#         "inputs": "address1",
#         "input_length": 1,
#         "description": "The contents of address1 is decremented",
#         "command": "$address1 -= 1"
#     },
#     "-11": {
#         "name": "subtract",
#         "inputs": "address1, address2, address3",
#         "input_length": 3,
#         "description": "The contents of address1 is subtracted from the contents of address2, the result is written to address3",
#         "command": "$address3 = $address2 - $address1"
#     },
#     "-12": {
#         "name": "multiply",
#         "inputs": "address1, address2, address3",
#         "input_length": 3,
#         "description": "The contents of address1 is multiplied by the contents of address2, the result is written to address3",
#         "command": "$address3 = $address1 * $address2"
#     },
#     "-13": {
#         "name": "free",
#         "inputs": "address1",
#         "input_length": 1,
#         "description": "The size of the working tape is decreased by the value found in address1",
#         "command": "working_tape = working_tape[:-$address1]"
#     }
# }