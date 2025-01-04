from sympy import gcd
import numpy as np
from scipy.optimize import linprog

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

# Sample OCN for tests
def get_sample_ocn():
    test_ocn1 = (5,1,2,[[1,'a',2,1],[2,'b',1,-1]])
    test_ocn2 = (3,1,2,[[1,'a',3,0],[2,'b',3,-2]])
    return test_ocn1,test_ocn2
 
# Sample Linear Path Scheme for tests   
def get_sample_path_scheme():
    test_scheme = [
        [
            [1, 2, 3, 4, -2, 1],
            [3, 4, 1, 2, -3, 4],
            [2, 1, 4, 3, 2, -1]
        ],
        [
            [4, 3, 2, 1, -3, 2],
            [2, 3, 4, 1, 4, -3],
            [1, 2, 3, 4, 1, -2]
        ],
        [
            [3, 4, 2, 1, -4, 3],
            [1, 3, 4, 2, 3, -1],
            [4, 2, 1, 3, -2, 4]
        ]
    ]
    return test_scheme

# Sample Linear Set for tests
def get_sample_linear_set():
    b = 8
    P = [
        [1, 2, 3],
        [3, 4, 1],
        [2, 3, 4]
    ]
    return b,P

# Reachability in Two-Dimensional Vector Addition Systems with States (PSPACE)
def ProduceLinPathScheme(p, q):
    # Dummy Linear Path Schema
    path_schemas = [[[[0,0,0,0,0,0]]]]    
    return path_schemas

# Checks if Intersection of L(A) and L(B) is empty
def check_disjointness(ocn1,ocn2):
    return True

# Unit test for checking disjointness
def test_disjointness():
    test_ocn1,test_ocn2=get_sample_ocn()
    assert check_disjointness(test_ocn1,test_ocn2)

# Helper function for Calculate_profile. This computes net effects by the alpha/beta sequence
# and minimum value of counter required to execute the sequence 
def compute_effect_and_min_counters(sequence):
    total_effect = [0, 0]  # Assuming counters are in 2D
    min_values = [0, 0]  # Minimal values
    
    for t in sequence:
        _, _,  _, _, counter1, counter2 = t
        
        # Update total effect
        total_effect[0] += counter1
        total_effect[1] += counter2
        # Update minimum counters
        min_values[0] = min(min_values[0], counter1)
        min_values[1] = min(min_values[1], counter2)
    
    return total_effect, min_values

# Returns 4k+2 integer pairs a,b,c,d given the Linear path schema
def calculate_profile(path_scheme):
    
    profile = {"a": [], "c": [], "b": [], "d": []}
    # a = Effects of alpha sequences
    # c = Minimun counter values for alpha sequence
    # b = Effects of beta sequences
    # d = Minimum counter values for beta sequence
    
    # Iterate through the linear path scheme
    index=0
    for sequence in path_scheme:
        effect, min_values = compute_effect_and_min_counters(sequence)
        min_counters=[0,0]
        min_counters[0] = max(0,0-min_values[0])
        min_counters[1] = max(0,0-min_values[1])
        if index%2 == 0:
            profile["a"].append(effect)
            profile["c"].append(min_counters)
        elif index%2 == 1:
            profile["b"].append(effect)
            profile["d"].append(min_counters)
        index=index+1
    
    return profile

# Unit test for Calculating profile - (4k+2) integers
def test_calculate_profile():
    test_scheme = get_sample_path_scheme()
    result = {'a': [[-3, 4], [-3, 6]], 'c': [[3, 1], [4, 1]], 'b': [[2, -3]], 'd': [[3, 3]]}
    assert calculate_profile(test_scheme) == result
    
def effect_in_alpha_sequence(profile, x, y, i):
    if x > profile['c'][i][0] and y > profile['c'][i][1]:
        x += profile['a'][i][0]
        y += profile['a'][i][1]
    return x,y

def effect_beta_sequence_in_first_quadrant(profile,i,x,y,bounds):
    

def calculate_linear_equations(profile, initial_counters, final_counters, bounds):
    k = max(len(profile["a"]), len(profile["b"]))  # Get the maximum length among alpha and beta sequences
    x = initial_counters[0]
    y = initial_counters[1]
    for i in range(k):
        # Check and iterate over alpha sequences (a[i], c[i]) if they exist
        if i < len(profile["a"]) and i < len(profile["c"]):
            x,y = effect_in_alpha_sequence(profile, x, y, i)
                
        # Check and iterate over beta sequences (b[i], d[i]) if they exist
        if i < len(profile["b"]) and i < len(profile["d"]):
            if profile['a'][i][0] > x and profile['a'][i][1] > y:
                effect_beta_sequence_in_first_quadrant(profile,i,x,y,bounds)
            if profile['a'][i][0] < x and profile['a'][i][1] > y:
                effect_beta_sequence_in_second_quadrant(profile,i,x,y,bounds)
            if profile['a'][i][0] < x and profile['a'][i][1] < y:
                effect_beta_sequence_in_third_quadrant(profile,i,x,y,bounds)
            if profile['a'][i][0] > x and profile['a'][i][1] < y:
                effect_beta_sequence_in_fourth_quadrant(profile,i,x,y,bounds)
            
def is_minimal(solution, solutions):
    """Check if a solution is minimal in the set."""
    for s in solutions:
        if np.all(solution >= s) and np.any(solution > s):
            return False
    return True

def get_bounds_for_LPS(cross_product):
    #Dummy return
    length_of_LPS = 10
    length_alpha = 10
    length_beta = 10
    return length_of_LPS,length_alpha,length_beta  


    
# Condition a of Lemma 19 
# Checks if first two coordinates are positive in any vector of P so that we get
# n1,n2 >= n for some linear combination
def check_if_first_two_coordinates_can_grow(P):
    found_positive_first = found_positive_second = False
    for vector in P:
        if vector[0] > 0:
            found_positive_first = True
        if vector[1] > 0:
            found_positive_second = True
        if found_positive_first and found_positive_second:
            return True
    return False # P cannot be constructed. Therefore it does not contain n-witness

# Unit test
def test_if_first_two_coordinates_can_grow():
    b3,P = get_sample_linear_set()
    assert check_if_first_two_coordinates_can_grow(P) == True

# Condition b of Lemma 19 using Proposition 20
# Checks if gcd of third coordinates of vectors in P divides b3
def check_if_b3_is_a_linear_combination_of_P3(b3,P):
    third_coords = [vector[2] for vector in P]
    # Calculate the gcd of all third coordinates
    g = gcd(third_coords)
    # Check if b3 is a multiple of this gcd
    if b3 % g == 0:
        return True
    
    return False  # g does not divide b3. Therefore it does not contain n-witness

# Unit test
def test_if_b3_is_a_linear_combination_of_P3():
    b3,P = get_sample_linear_set()
    assert check_if_b3_is_a_linear_combination_of_P3(b3,P) == True

# Lemma 19 : Checks if the linear set L = b3 + P* contains n-witnesses for all n>0
def check_n_witness(b3,P):
    return check_if_first_two_coordinates_can_grow(P) and check_if_b3_is_a_linear_combination_of_P3(b3,P)
        
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

    for p,q in cross_product_automaton.states:
        Lin_Path_Schemes=ProduceLinPathScheme((0,0),(p,q))
        for scheme in Lin_Path_Schemes:
            profile = calculate_profile(scheme)
            result = calculate_linear_equations(profile,[p,q])
            

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

    # test_disjointness()
    # test_calculate_profile()
    # test_if_first_two_coordinates_can_grow()
    # test_if_b3_is_a_linear_combination_of_P3()