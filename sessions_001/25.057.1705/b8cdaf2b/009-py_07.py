import numpy as np
input_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1]
])
output_grid = np.array([
    [3, 0, 0, 0, 0, 0, 3],
    [0, 3, 0, 0, 0, 3, 0],
    [0, 0, 3, 0, 3, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1]

])
result_grid = transform(input_grid)
print(np.array_equal(result_grid, output_grid))