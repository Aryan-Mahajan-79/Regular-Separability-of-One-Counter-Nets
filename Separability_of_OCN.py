import numpy as np
from scipy.optimize import linprog
import numpy as np
import Algebraic_operations as lin_alg
import Linear_path_schema_and_profile as lps
from Linear_equations import *

# Definition of One Counter Nets (Q, α0, αf, T; T=0) where T=0 is empty set
class OneCounterNet:
    def __init__(self, num_states, initial_state, final_state, transitions):
        self.num_states = num_states        # No. of states
        self.initial_state = initial_state  # Initial state of OCN (counter value zero)
        self.final_state = final_state      # Final state of OCN (counter value zero)
        self.transitions = transitions      # Transitions of OCN {Initial State, Label, Final State, Effect}

    # Display the OCN states and transitions
    def display(self):
        state_size=self.num_states
        print(f"{state_size}")
        for state in self.states:
            print(state)
        transition_size=len(self.transitions)
        print(f"{transition_size}")
        for transition in self.transitions:
            print(transition)
            
# Definition of Cross Product operation over two One Counter Nets
class CrossProduct:
    def __init__(self, OCN_A, OCN_B):
        self.A = OCN_A
        self.B = OCN_B
        self.states = set()  # States of the cross-product automaton
        self.transitions = set()  # Transitions of the cross-product automaton

    def compute_cross_product(self):
        # Set of states as pairs of states from both automata
        for state_A in range(1,self.A.num_states+1):
            for state_B in range(1,self.B.num_states+1):
                self.states.add((state_A, state_B))  # Cross-product states (q, p)

        # Transitions based on the cross-product rule
        for (q, a, q1, z) in self.A.transitions:
            for (p, a2, p1, v) in self.B.transitions:
                if a == a2:  # Synchronize transitions on the same input symbol
                    # Add the cross-product transition: (q, p) -> (q1, p1) with counter changes (z, v)
                    self.transitions.add(((q, p), (q1, p1), (z, v)))

        # Zero-transitions for each state
        for state_A in range(1,self.A.num_states+1):
            for state_B in range(1,self.B.num_states+1):
                self.transitions.add(((state_A, state_B), (state_A, state_B), (0, 0)))

    # Display the Cross Product on Terminal
    def display(self):
        state_size=len(self.states)
        transition_size=len(self.transitions)
        print(f"{state_size}")
        for state in self.states:
            print(state)
        print(f"{transition_size}")
        for transition in self.transitions:
            print(transition)
            
    # Display the cross product in a text file
    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            # Write the states of the cross-product automaton
            state_size=len(self.states)
            transition_size=len(self.transitions)
            file.write(f"{state_size}\n")
            for state in self.states:
                file.write(f"{state[0]},{state[1]}\n")
            
            # Write the transitions of the cross-product automaton
            file.write(f"{transition_size}\n")
            for transition in self.transitions:
                file.write(f"{transition[0][0]},{transition[0][1]},{transition[1][0]},{transition[1][1]},{transition[2][0]},{transition[2][1]}\n")

# Returns an OCN from the input file provided
def parse_ocn(file_path):
    """
    Parses an OCN definition from a file.
    File format:
        - Number of states
        - Initial state
        - Final state
        - Transitions: start_state, symbol, counter_effect, end_state
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    num_states = int(lines[0].strip())
    initial_state = int(lines[1].strip())
    final_state = int(lines[2].strip())
    transitions = []

    for line in lines[3:]:
        start_state, symbol, counter_effect, end_state = line.strip().split(',')
        transitions.append((int(start_state), symbol, int(counter_effect), int(end_state)))

    return OneCounterNet(num_states, initial_state, final_state, transitions)



# Checks if Intersection of L(A) and L(B) is empty
def check_disjointness(ocn1,ocn2):
    return True

     
# Checks if the two OCN are separable or not
def check_separability(ocn1,ocn2):
        
    is_disjoint = check_disjointness(ocn1,ocn2)
    if not is_disjoint:
        return False
    # If not disjoint we proceed (Assumption 12)
    
    cross_product_automaton = CrossProduct(ocn1, ocn2)
    cross_product_automaton.compute_cross_product()
    # cross_product_automaton.display()                                 # Uncomment to display the states and transitions of the cross-product
    # cross_product_automaton.write_to_file("cross_product_output.txt") # Uncomment to display the cross-product in text file

    # For PREF (0,0)->(p,q)
    for p,q in cross_product_automaton.states:
        # Get the linear path schemes for PREF from (0,0) to (p,q)
        # It is a Reachability in 2-VASS
        Lin_Path_Schemes=lps.ProduceLinPathScheme((0,0),(p,q))
        
        for scheme in Lin_Path_Schemes:
            
            # For each scheme calculate its profile: 4k+2 integers representing the effects of transitions
            # and minimum counter value required for the alpha/beta transition
            profile = lps.calculate_profile(scheme)
            
            # Get the constraints and effects of transition to check if the transition is possible or not
            result = calculate_linear_equations(profile,[p,q])
            
            # Returns a semi-linear set of the form B+P* for finite sets B,P
            semi_linear_set = lin_alg.calculate_semi_linear_set(result)  # Linear Algebra Operations
            
            lin_alg.enumerate_semi_linear_set(semi_linear_set)
    
    # For SUFF (p,q)->(0,0)
    # Same as done for PREF, only initial and final states are reversed
    for p,q in cross_product_automaton.states:
        Lin_Path_Schemes=lps.ProduceLinPathScheme((p,q),(0,0))
        for scheme in Lin_Path_Schemes:
            profile = lps.calculate_profile(scheme)
            result = calculate_linear_equations(profile,[p,q])
            semi_linear_set = lin_alg.calculate_semi_linear_set(result)
            lin_alg.enumerate_semi_linear_set(semi_linear_set)
    
            

if __name__ == "__main__":
    file1 = "./ocn1.txt"
    file2 = "./ocn2.txt"
    ocn1 = parse_ocn(file1)
    ocn2 = parse_ocn(file2)
    is_separable = check_separability(ocn1, ocn2)
    if is_separable:
        print("The One Counter Nets are separable")
    else:
        print("The One Counter Nets are not separable")
