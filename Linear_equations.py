import numpy as np

def effect_in_alpha_sequence(profile, counters, i):
    
    if np.all(counters > profile['alpha_min_count'][i]):
        counters += profile['alpha_effect'][i]

    return counters


# Case 1 : Beta transition effect moves counter towards first quadrant
def effect_beta_sequence_in_first_quadrant(profile, i, counters, k):
    
    counters = np.array(counters)
    beta_min_count = np.array(profile['beta_min_count'][i + 1])
    beta_effect = np.array(profile['beta_effect'][i + 1])

    # Constraint : [x1 y1] > M_2 (min counter)
    if np.all(counters > beta_min_count):
        # Effect : [x2 y2] = [x1 y1] + (k * E_2)
        counters += k * beta_effect

    return counters

# Case 2 : Beta transition effect moves counter towards second quadrant
def effect_beta_sequence_in_second_quadrant(profile, i, counters, k):

    beta_min_vector = np.array(profile['beta_min_count'][i + 1])
    beta_effect_vector = np.array(profile['beta_effect'][i + 1])
    
    # Computes the next counters if constraint is satisfied
    counters_next = counters + k * beta_effect_vector
    
    # Constraints: [x1, y1] > M_2 and [x2, y2] - E_2 > M_2
    if (np.all(counters > beta_min_vector) and 
        np.all(counters_next - beta_effect_vector > beta_min_vector)):
        # Effect: [x2, y2] = [x1, y1] + k * E_2
        counters = counters_next

    return counters

# Case 3 : Beta transition effect moves counter towards third quadrant
def effect_beta_sequence_in_third_quadrant(profile, i, counters, k):
    beta_min_vector = np.array(profile['beta_min_count'][i + 1])
    beta_effect_vector = np.array(profile['beta_effect'][i + 1])
    
    # Computes the next counters if constraint is satisfied
    counters_next = counters + k * beta_effect_vector
    
    # Constraint: [x2, y2] - E_2 > M_2
    if np.all(counters_next - beta_effect_vector > beta_min_vector):
        # Effect: [x2, y2] = [x1, y1] + k * E_2
        counters = counters_next

    return counters

# Case 4 : Beta transition effect moves counter towards fourth quadrant
# This case is same as second quadrant case 
def effect_beta_sequence_in_fourth_quadrant(profile, i, counters, k):
    # function calls second quadrant as constraint and effects are same
    return effect_beta_sequence_in_second_quadrant(profile, i, counters, k)


def calculate_linear_equations(profile, initial_counters, final_counters, bounds):
    n = len(profile['alpha_effect'])
    k = 10
    counters = np.array(initial_counters)  # Represent counters as a vector [x, y]
    # profile = np.array(profile)
    
    if n < bounds[0]:
        for i in range(n):
            # Check and iterate over alpha sequences (alpha_effect[i], alpha_min_counter[i]) if they exist
            counters = effect_in_alpha_sequence(profile, counters, i)
            
            # Check and iterate over beta sequences (beta_efect[i], beta_min_count[i]) if they exist
            if i < len(profile['beta_effect']) - 1 and i < len(profile['beta_min_count']) - 1:
                beta_effect_vector = np.array(profile['beta_effect'][i])
                
                if np.all(beta_effect_vector > counters) and k < bounds[1]:
                    counters = effect_beta_sequence_in_first_quadrant(profile, i, counters, k)
                elif beta_effect_vector[0] < counters[0] and beta_effect_vector[1] > counters[1] and k < bounds[1]:
                    counters = effect_beta_sequence_in_second_quadrant(profile, i, counters, k)
                elif np.all(beta_effect_vector < counters) and k < bounds[1]:
                    counters = effect_beta_sequence_in_third_quadrant(profile, i, counters, k)
                elif beta_effect_vector[0] > counters[0] and beta_effect_vector[1] < counters[1] and k < bounds[1]:
                    counters = effect_beta_sequence_in_fourth_quadrant(profile, i, counters, k)
    
    final_counters = tuple(counters)
    return final_counters

