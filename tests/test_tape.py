from tm.tape import Tape

def test_tape():
    print("TESTING Tape")
    tape = Tape()    # [program_tape][working_tape]
    
    # Test append
    print("\nTesting Append Fns")
    tape.append_to_working_tape('a')
    print("Working append 'a': ", tape) # [][a]

    tape.append_to_working_tape('b')
    print("Working append 'b': ", tape) # [][a, b]
    
    tape.append_to_program_tape('1')
    print("Program append '1': ", tape) # [1][a, b]
    
    tape.append_to_program_tape('2')
    print("Program append '2': ", tape) # [2, 1][a, b]
       # Index:   -2,-1, 0, 1

    # Test len
    print("\nTesting Length Fns")
    print("tape.length_of_working_tape(): ", tape.working_tape_length())  # Output: 2
    print("tape.length_of_program_tape(): ", tape.program_tape_length())  # Output: 2

    # Test positive index access
    print("\nTesting Positive Indexing")
    print("tape[0] = ", tape[0])    # Output: 'a'
    print("tape[1] = ", tape[1])    # Output: 'b'
    print("tape[2] = ", tape[2])    # Output: None

    # Test negative index access
    print("\nTesting Negative Indexing")
    print("tape[-1] = ", tape[-1])   # Output: '2'
    print("tape[-2] = ", tape[-2])   # Output: '1'
    print("tape[-3] = ", tape[-3])   # Output: None


    # Test pop
    print("\nTesting Pop Fns")
    print("tape.pop_from_working_tape(): ", tape.pop_from_working_tape())  # Output: 'b'
    print("tape.pop_from_program_tape(): ", tape.pop_from_program_tape())  # Output: '2'
    print("tape.pop_from_working_tape(): ", tape.pop_from_working_tape())  # Output: 'a'
    print("tape.pop_from_program_tape(): ", tape.pop_from_program_tape())  # Output: '1'
    print("tape.pop_from_working_tape(): ", tape.pop_from_working_tape())  # Output: None
    print("tape.pop_from_program_tape(): ", tape.pop_from_program_tape())  # Output: None
