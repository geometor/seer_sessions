import numpy as np

input_grid = np.array([[1, 1, 1],
                       [1, 2, 1],
                       [1, 1, 1]])
expected_output = np.array([[1, 1, 1],
                            [1, 2, 1],
                            [1, 1, 1]])
output_grid = transform(input_grid)
print(np.array_equal(output_grid,expected_output))
#check neighbors of center, should be all 1
print(get_neighbors(input_grid,1,1))