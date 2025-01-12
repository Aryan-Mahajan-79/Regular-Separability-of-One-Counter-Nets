import numpy as np

def effect_in_alpha_sequence(profile, counters, i):
    
    if np.all(counters > profile['alpha_min_count'][i]):
        counters += profile['alpha_effect'][i]

    return counters


# Case 1 : Beta transition effect moves counter towards first quadrant
def effect_beta_sequence_in_first_quadrant(profile, i, counters, k):
    
    # Constraint : [x1 y1] > M_2 (min counter)
    if np.all(counters > profile['beta_min_count'][i + 1]):
        
        # Effect : [x2 y2] = [x1 y1] + (k * E_2)  (effect of transition once running k loops)
        counters += k * profile['beta_effect'][i + 1]

    return counters

# Case 2 : Beta transition effect moves counter towards second quadrant
def effect_beta_sequence_in_second_quadrant(profile, i, counters, k):

    beta_min_vector = profile['beta_min_count'][i + 1]
    beta_effect_vector = profile['beta_effect'][i + 1]
    
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
    beta_min_vector = profile['beta_min_count'][i + 1]
    beta_effect_vector = profile['beta_effect'][i + 1]
    
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
    n = max(len(profile['alpha_effect']), len(profile['beta_effect']))  # Get the maximum length among alpha and beta sequences
    k = 10
    counters = np.array(initial_counters)  # Represent counters as a vector [x, y]
    profile = np.array(profile)
    
    if n < bounds[0]:
        for i in range(n):
            # Check and iterate over alpha sequences (a[i], c[i]) if they exist
            if i < len(profile['alpha_effect']) and i < len(profile['alpha_min_count']):
                counters = effect_in_alpha_sequence(profile, counters, i)
            
            # Check and iterate over beta sequences (b[i], d[i]) if they exist
            if i < len(profile['beta_effect']) - 1 and i < len(profile['beta_min_count']) - 1:
                alpha_effect_vector = np.array(profile['alpha_effect'][i])
                
                if np.all(alpha_effect_vector > counters) and k < bounds[1]:
                    counters = effect_beta_sequence_in_first_quadrant(profile, i, counters, k)
                elif alpha_effect_vector[0] < counters[0] and alpha_effect_vector[1] > counters[1] and k < bounds[1]:
                    counters = effect_beta_sequence_in_second_quadrant(profile, i, counters, k)
                elif np.all(alpha_effect_vector < counters) and k < bounds[1]:
                    counters = effect_beta_sequence_in_third_quadrant(profile, i, counters, k)
                elif alpha_effect_vector[0] > counters[0] and alpha_effect_vector[1] < counters[1] and k < bounds[1]:
                    counters = effect_beta_sequence_in_fourth_quadrant(profile, i, counters, k)
    
    final_counters = tuple(counters)
    return final_counters

