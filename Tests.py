from Separability_of_OCN import *
from Sample_Inputs import *

# Unit test for checking disjointness
def test_disjointness():
    test_ocn1,test_ocn2=get_sample_ocn()
    assert check_disjointness(test_ocn1,test_ocn2)
    
def test_effect_in_alpha_sequence():
    profile = get_sample_profile()
    
    x, y = 5, 6
    i = 0
    result = effect_in_alpha_sequence(profile, x, y, i)
    assert result == (6, 7)

def test_effect_beta_sequence_in_first_quadrant():
    profile = get_sample_profile()

    x, y, i, k = 7, 8, 0, 2
    result = effect_beta_sequence_in_first_quadrant(profile, i, x, y, k)
    assert result == (11, 12)
    
def test_effect_beta_sequence_in_second_quadrant():
    profile = get_sample_profile()

    x, y, i, k = 3, 2, 0, 2
    result = effect_beta_sequence_in_second_quadrant(profile, i, x, y, k)
    assert result == (3, 2)

# test_effect_beta_sequence_in_third_quadrant is same as test_effect_beta_sequence_in_second_quadrant

def test_effect_beta_sequence_in_fourth_quadrant():

    profile = get_sample_profile()
    x, y, i, k = 7, 8, 1, 3
    result = effect_beta_sequence_in_fourth_quadrant(profile, i, x, y, k)
    assert result == (16, 17)

def test_calculate_linear_equations():
    profile = {
        "a": [[1, 2], [2, -3], [3, 4]],
        "b": [[1, 1], [1, 1], [1, 1]],
        "c": [[2, -3], [3, 4], [-4, 5]],
        "d": [[1, 1], [-2, 2], [-3, 3]]
    }
    bounds = [10, 20]

    initial_counters = (3, 4)
    final_counters = (0, 0)
    result = calculate_linear_equations(profile, initial_counters, final_counters, bounds)
    assert result == (29, 27)

# Unit test
def test_if_first_two_coordinates_can_grow():
    b3,P = get_sample_linear_set()
    assert check_if_first_two_coordinates_can_grow(P) == True


# Unit test
def test_if_b3_is_a_linear_combination_of_P3():
    b3,P = get_sample_linear_set()
    assert check_if_b3_is_a_linear_combination_of_P3(b3,P) == True

# if __name__ == "__main__":
    
#     test_disjointness()
#     test_calculate_profile()
#     test_if_first_two_coordinates_can_grow()
#     test_if_b3_is_a_linear_combination_of_P3()