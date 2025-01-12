from sympy import gcd
from itertools import product
import numpy as np

def calculate_semi_linear_set(result):
    B = []
    P = []
    return B,P

def enumerate_semi_linear_set(semi_linear_set):
    B = semi_linear_set[0]
    P = semi_linear_set[1]
    
    product_list = []

    # Filter all base vectors in B 
    valid_bases = [b for b in B]

    # Filter all period vectors in P 
    valid_periods = [p for p in P]

    # Generate all valid (b, p) pairs
    for b, p in product(valid_bases, valid_periods):
        product_list.append((b, p))

    return product_list
    
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

# Lemma 19 : Checks if the linear set L = b3 + P* contains n-witnesses for all n>0
def check_n_witness(b3,P):
    return check_if_first_two_coordinates_can_grow(P) and check_if_b3_is_a_linear_combination_of_P3(b3,P)
   
            
def is_minimal(solution, solutions):
    # Check if a solution is minimal in the set.
    for s in solutions:
        if np.all(solution >= s) and np.any(solution > s):
            return False
    return True
