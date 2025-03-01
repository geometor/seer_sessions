import numpy as np
input_grid = np.array([[1, 1, 0, 0, 0],
                        [1, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1]])
expected_output = np.array([[1, 1, 0, 0, 0],
                            [1, 0, 0, 0, 0],
                            [1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 2]])
output_grid = transform(input_grid)
print(np.array_equal(output_grid,expected_output))
# check the lower right corner, it should have no neighbors
print(get_neighbors(input_grid,4,4))