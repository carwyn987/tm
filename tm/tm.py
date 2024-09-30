from tm.tape import Tape

class TM:
    def __init__(self):
        # Define tapes
        self.program_working_tape = Tape()
        self.input_tape = []
        self.output_tape = []

        # Define "pointers"
        self.input_ptr_idx = 0
        self.program_ptr_idx = -1 # This pointer is required to stay negative in program space
        # Output tape 'pointer' is always at end, no need to define an indx

        # Logging
        self.save_ran_instructions = []

    def setup_program(self, program):
        self.program_working_tape.program_tape = program # replace with setter

    def setup_inputs(self, inputs):
        self.input_tape = inputs

    def apply(self):
        """
        Return Values:
        --------------
        -  0: Success
        - -1: Failure
        -  1: Halt
        """
        instruction_number = self.program_working_tape[self.program_ptr_idx]
        self.save_ran_instructions.append(instruction_number)

        # Try to apply current program instruction
        try:
            match instruction_number:
                case -1:
                    # jumpleq(address1, address2, address3)
                    # If the contents of address1 is less than or equal to the contents of address2, the InstructionPointer is set equal to address3
                    if not self.program_working_tape[self.program_ptr_idx-1] <= self.program_working_tape[self.program_ptr_idx-2]:
                        move_forward = 4
                    elif self.program_working_tape[self.program_ptr_idx-3] is not None and self.program_working_tape[self.program_ptr_idx-3] < 0:
                        self.program_ptr_idx = self.program_working_tape[self.program_ptr_idx-3]
                        move_forward = 0 # CONDITIONAL
                    else:
                        raise IndexError()
                case -2:
                    # output(address1)
                    # A primitive for interaction with the external environment. It corresponds to the TM action of "writing the output tape"
                    self.output_tape.append(self.program_working_tape[self.program_ptr_idx-1])
                    move_forward = 2
                case -3:
                    # jump(address1)
                    # The InstructionPointer is set equal to address1
                    if self.program_working_tape[self.program_ptr_idx-1] is not None and self.program_working_tape[self.program_ptr_idx-1] < 0:
                        self.program_ptr_idx = self.program_working_tape[self.program_ptr_idx-1]
                        move_forward = 0
                    else:
                        raise IndexError()
                case -4:
                    # stop()
                    # Halt the current program
                    return 1
                case -5:
                    # add(address1, address2, address3)
                    # The contents of address1 is added to the contents of address2, the result is written into address3
                    self.program_working_tape[self.program_ptr_idx-3] = self.program_working_tape[self.program_ptr_idx-1] + self.program_working_tape[self.program_ptr_idx-2]
                    move_forward = 4
                case -6:
                    # getInput(address1, address2)
                    # Reads the current value of the ith input (value at address1) into address2.
                    self.program_working_tape[self.program_ptr_idx-2] = self.input_tape[self.program_working_tape[self.program_ptr_idx-1]]
                    move_forward = 3
                case -7:
                    # move(address1, address2)
                    # The contents of address1 is copied into address2
                    self.program_working_tape[self.program_ptr_idx-2] = self.program_working_tape[self.program_ptr_idx-1]
                    move_forward = 3
                case -8:
                    # Increment(address1) - on working tape
                    # The contents of address1 is incremented
                    self.program_working_tape[self.program_working_tape[self.program_ptr_idx-1]] += 1
                    move_forward = 2
                case -9:
                    # Decrement(address1) - on working tape
                    # The contents of address1 is decremented
                    self.program_working_tape[self.program_working_tape[self.program_ptr_idx-1]] -= 1
                    move_forward = 2
                case -10:
                    # subtract(address1, address2, address3)
                    # The contents of address1 is subtracted from the contents of address2, the result is written to address3
                    self.program_working_tape[self.program_ptr_idx-3] = self.program_working_tape[self.program_ptr_idx-1] - self.program_working_tape[self.program_ptr_idx-2]
                    move_forward = 4
                case -11:
                    # multiply(address1, address2, address3)
                    # The contents of address1 is multiplied by the contents of address2, the result is written to address3
                    self.program_working_tape[self.program_ptr_idx-3] = self.program_working_tape[self.program_ptr_idx-1] * self.program_working_tape[self.program_ptr_idx-2]
                    move_forward = 4
                # case -12:
                #     # free(address1)
                #     # The size of the workig tape is decreased by the value found in address1. Min is updated accordingly.
                #     num_free = self.program_working_tape[self.program_ptr_idx-1]
                #     if num_free < 0:
                #         num_free = 0
                #     elif num_free > 5:
                #         num_free = 5
                #     self.program_working_tape.working_tape = self.program_working_tape.working_tape[:-num_free]
                    
                #     move_forward = 2
                # case -13:
                #     # allocate(address1)
                #     # The size of the working tape is increased by the value found in address1, initializing all cells to zero. Allocate is limited to 5 at any one invocation.
                #     num_increase = self.program_working_tape[self.program_ptr_idx-1]
                #     if num_increase < 0:
                #         pass
                #     elif num_increase > 5:
                #         num_increase = 5
                    
                #     for _ in range(num_increase):
                #         self.program_working_tape.working_tape.append(0)
                    
                #     move_forward = 2
                case _:
                    raise NotImplementedError()
            
        except:
            # Executing program instruction failed
            return -1.
            
        # Move program pointer
        self.program_ptr_idx += -1*move_forward

        # Check bounds of program
        if self.program_working_tape[self.program_ptr_idx] is None:
            return 1.
        
        # Executed correctly and still within program bounds
        return 0.
    
    def run(self, max_steps, fitness_fn, labels):
        """
        Run tm until final state

        Returns:
        ----------
         - fitness (float): Computed fitness between output tape and expected output, according to passed in or default fitness function
         - final_status (int): 0 = running, 1 = halted, -1 = failure to apply
        """

        iters = 0
        response = self.apply()
        # While running and less than max_steps
        while response != -1 and response != 1 and iters < max_steps:
            iters += 1
            response = self.apply()

        # Now that run is complete, parse response
        fitness = fitness_fn(self.output_tape, labels)
            
        return fitness, response, iters