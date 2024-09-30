class Tape:
    """
    This class represents the combination of a Turing Machine working and program tape.

    It is set up to be interacted with as a single list, with indices >=0 accessing the working tape, and indices < 0 accessing the program tape.
    E.g.

    TYPE:               |      Program Tape            Working Tape
    TAPE RELATIVE INDEX:|    3     2     1     0     0      1     2     3
    TAPE:               |  [ITEM, ITEM, ITEM, ITEM][ITEM, ITEM, ITEM, ITEM]
    ABSOLUTE INDEX:     |   -4    -3    -2    -1     0      1     2     3
    """
    
    def __init__(self):
        self.working_tape = []
        self.program_tape = []

    def append_to_working_tape(self, item):
        self.working_tape.append(item)

    def append_to_program_tape(self, item):
        self.program_tape.append(item)

    def pop_from_working_tape(self):
        return self.working_tape.pop() if self.working_tape else None

    def pop_from_program_tape(self):
        return self.program_tape.pop() if self.program_tape else None

    def __getitem__(self, index):
        if index >= 0:
            if index < len(self.working_tape):
                return self.working_tape[index]
            else:
                return None
        else:
            index = abs(index) - 1
            if index < len(self.program_tape):
                return self.program_tape[index]
            else:
                return None

    def __setitem__(self, index, value):
        if index >= 0:
            if index < len(self.working_tape):
                self.working_tape[index] = value
            else:
                raise IndexError("Out of bounds")
        else:
            index = abs(index) - 1
            if index < len(self.program_tape):
                self.program_tape[index] = value
            else:
                raise IndexError("Out of bounds")

    def __str__(self):
        return str(list(reversed(self.program_tape))) + str(self.working_tape)
    
    def verbose(self):
        s = (
            "Program Tape: " + str(self.program_tape) + "\n"
            "Working Tape: " + str(self.working_tape) + "\n"
            "Number Line Indexed: " + str(list(reversed(self.program_tape))) + str(self.working_tape)
            )
        return s
    
    def working_tape_length(self):
        return len(self.working_tape)

    def program_tape_length(self):
        return len(self.program_tape)
