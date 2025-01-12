

# Reachability in Two-Dimensional Vector Addition Systems with States (PSPACE)
def ProduceLinPathScheme(p, q):
    # Dummy Linear Path Schema
    path_schemas = [[[[0,0,0,0,0,0]]]]    
    return path_schemas

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
    
    profile = {'alpha_effect': [], 'alpha_min_count': [], 'beta_effect': [], 'beta_min_count': []}
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
            profile['alpha_effect'].append(effect)
            profile['alpha_min_count'].append(min_counters)
        elif index%2 == 1:
            profile['beta_effect'].append(effect)
            profile['beta_min_count'].append(min_counters)
        index=index+1
    
    return profile


# Lemma 22 :
# Length of Linear Path Schema is bounded where bound is exponential
# Lenght of loops is bounded where bound is polynomial
def get_bounds_for_LPS(cross_product):
    #Dummy return
    length_of_LPS = 10   # exponential
    length_loop = 10     # polynomial
    return length_of_LPS,length_loop 
