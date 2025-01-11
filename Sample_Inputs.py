
# Sample OCN for tests
def get_sample_ocn():
    test_ocn1 = (5,1,2,[[1,'alpha_effect',2,1],[2,'beta_effect',1,-1]])
    test_ocn2 = (3,1,2,[[1,'alpha_effect',3,0],[2,'beta_effect',3,-2]])
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

def get_sample_profile():
    profile = {
        'alpha_min_count': [[2, 3], [4, 5], [6, 7]],
        'alpha_effect': [[1, 1], [2, 2], [3, 3]],
        'beta_min_count': [[2, 3], [4, 5], [6, 7]],
        'beta_effect': [[1, 1], [2, 2], [3, 3]]
    }
    return profile